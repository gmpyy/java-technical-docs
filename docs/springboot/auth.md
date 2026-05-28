---
title: "JWT 与验证码认证"
description: "JWT 登录流程、Token 生成和校验、Session 验证码与登录校验"
outline: [2, 4]
---

# JWT 与验证码认证

这一章对应 `JAVA.md` 中“JWT 鉴权”和“session 实现验证码验证”两部分。这里保留 JWT 登录、客户端携带 Token、拦截器校验 Token、Session 验证码生成与登录校验流程。

## JWT 鉴权

![JWT 鉴权流程](/java-technical-docs/images/source/image-19.png)

认证链路的核心是：

```text
用户登录成功
  -> 服务端生成 JWT
  -> Controller 把 Token 返回给客户端
  -> 客户端后续请求携带 Authorization: Bearer <token>
  -> 服务端拦截器统一校验 Token
  -> 校验通过放行，失败返回 401
```

## 登录阶段：生成 Token

登录成功后，服务端生成 JWT。核心点有三个：

- **sub（Subject）**：一般存用户唯一标识，如用户名或 `userId`
- **iat（Issued At）**：签发时间
- **exp（Expiration）**：过期时间

### JwtUtil 生成 Token

下面是一个典型的 `generateToken` 生成逻辑：

```java
public String generateToken(String subject) {
    Date now = new Date();
    Date expiry = new Date(now.getTime() + expiration * 1000);

    return Jwts.builder()
            .setSubject(subject)
            .setIssuedAt(now)
            .setExpiration(expiry)
            .signWith(secretKey, SignatureAlgorithm.HS256)
            .compact();
}
```

### AuthService 登录成功后生成 Token

真正生成 Token 的逻辑发生在 `AuthService.login`：先校验账号密码，再调用 `JwtUtil.generateToken`，并把 Token 放进响应对象。

```java
public UserLoginResponse login(UserLoginRequest request) {
    UserLoginResponse response = new UserLoginResponse();

    if (request == null || isBlank(request.getUsername()) || isBlank(request.getPassword())) {
        response.setSuccess(false);
        response.setMessage("参数不完整");
        return response;
    }

    UserEntity user = userRepository.findByUsernameAndPassword(
            request.getUsername(),
            request.getPassword());

    if (user == null) {
        response.setSuccess(false);
        response.setMessage("用户名或密码错误");
        return response;
    }

    response.setId(user.getId());
    response.setUsername(user.getUsername());
    response.setSuccess(true);
    response.setMessage("登录成功");
    response.setToken(jwtUtil.generateToken(user.getUsername()));
    return response;
}
```

关键点：Token 的生成在 Service 层完成，Controller 只是把它写到响应头或响应体里。

### AuthController 登录成功后返回 Token

登录接口在响应头里写入 `Authorization`：

```java
@PostMapping("/login")
public ResponseEntity<UserLoginResponse> login(@RequestBody UserLoginRequest request) {
    UserLoginResponse response = authService.login(request);

    if (response.isSuccess() && response.getToken() != null) {
        return ResponseEntity.ok()
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + response.getToken())
                .body(response);
    }

    return ResponseEntity.ok(response);
}
```

这样客户端登录成功后就能拿到 JWT。

## 客户端请求阶段：携带 Token

客户端每次访问受保护接口时，需要携带：

```http
Authorization: Bearer <token>
```

示例请求：

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6..." \
  http://localhost:8080/api/user/profile
```

只要带着正确的 Token，服务端就可以从中识别用户身份。

## 服务端校验阶段：拦截器校验 Token

本项目使用 `HandlerInterceptor` 统一拦截 `/api/**` 请求进行校验。

### 拦截器的整体流程

1. 读取请求头 `Authorization`。
2. 校验格式是否为 `Bearer <token>`。
3. 解析并验证 Token，包括签名、过期时间和格式合法性。
4. 校验通过则放行。

### JwtAuthInterceptor 关键逻辑

```java
@Override
public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
        throws IOException {
    String header = request.getHeader(HttpHeaders.AUTHORIZATION);

    if (header == null || !header.startsWith("Bearer ")) {
        writeUnauthorized(response, "Unauthorized");
        return false;
    }

    String token = header.substring("Bearer ".length()).trim();
    if (token.isEmpty()) {
        writeUnauthorized(response, "Unauthorized");
        return false;
    }

    try {
        jwtUtil.validateToken(token);
    } catch (JwtException | IllegalArgumentException ex) {
        writeUnauthorized(response, "Invalid token");
        return false;
    }

    return true;
}
```

### JwtUtil 校验 Token

```java
public void validateToken(String token) {
    Jwts.parserBuilder()
            .setSigningKey(secretKey)
            .build()
            .parseClaimsJws(token);
}
```

只要解析失败，比如过期、签名错误、格式非法，就会抛出异常并返回 401。

## Session 实现验证码验证

![Session 验证码流程 1](/java-technical-docs/images/source/image-20.png)

![Session 验证码流程 2](/java-technical-docs/images/source/image-21.png)

验证码的核心流程：

```text
客户端请求验证码
  -> 服务端生成随机码
  -> 生成验证码图片
  -> 把验证码和过期时间写入 Session
  -> 返回 Base64 图片
  -> 登录时提交账号、密码、验证码
  -> 服务端从 Session 取验证码并校验
```

## 获取验证码：生成图片 + 写入 Session

### 新增接口：`POST /api/auth/captcha`

Controller 直接调用 `AuthService.generateCaptcha`：

```java
@PostMapping("/captcha")
public CaptchaResponse captcha(HttpSession session) {
    return authService.generateCaptcha(session);
}
```

### AuthService 生成验证码并存入 Session

核心逻辑：

1. 生成随机码和图片。
2. 设置过期时间。
3. 存入 Session。
4. 返回 Base64 和过期时间。

```java
public CaptchaResponse generateCaptcha(HttpSession session) {
    CaptchaUtil.CaptchaResult result = CaptchaUtil.generateCaptcha(CAPTCHA_LENGTH);
    long expiresAt = System.currentTimeMillis() + CAPTCHA_EXPIRE_MILLIS;

    session.setAttribute(SESSION_CAPTCHA_CODE, result.getCode());
    session.setAttribute(SESSION_CAPTCHA_EXPIRES_AT, expiresAt);

    return new CaptchaResponse(result.getImageBase64(), expiresAt);
}
```

### CaptchaUtil 生成 Base64 图片

生成步骤：

- 生成随机码，排除易混淆字符。
- 绘制到图片。
- 生成 Base64 字符串。

```java
public static CaptchaResult generateCaptcha(int length) {
    String code = randomCode(length);
    BufferedImage image = renderImage(code, 120, 40);
    String base64 = encodeBase64(image);
    return new CaptchaResult(code, base64);
}
```

## 登录时校验验证码

### 登录请求增加 `captcha` 字段

```java
private String captcha;
```

### AuthService 在登录前做验证码校验

校验规则：

- Session 无验证码：认为过期。
- 超过 5 分钟：过期。
- 不匹配：忽略大小写后仍不相同则错误。
- 校验成功：移除 Session 中的验证码，然后继续登录。

```java
if (request == null
        || isBlank(request.getUsername())
        || isBlank(request.getPassword())
        || isBlank(request.getCaptcha())) {
    response.setSuccess(false);
    response.setMessage("参数不完整");
    return response;
}

String sessionCode = (String) session.getAttribute(SESSION_CAPTCHA_CODE);
Long expiresAt = (Long) session.getAttribute(SESSION_CAPTCHA_EXPIRES_AT);

if (sessionCode == null || expiresAt == null) {
    response.setSuccess(false);
    response.setMessage("验证码已过期");
    return response;
}

if (System.currentTimeMillis() > expiresAt) {
    response.setSuccess(false);
    response.setMessage("验证码已过期");
    return response;
}

if (!sessionCode.equalsIgnoreCase(request.getCaptcha())) {
    response.setSuccess(false);
    response.setMessage("验证码错误");
    return response;
}

session.removeAttribute(SESSION_CAPTCHA_CODE);
session.removeAttribute(SESSION_CAPTCHA_EXPIRES_AT);
```

校验通过后，继续执行原有账号密码登录逻辑。

## 本章检查

- 能说清 JWT 的 `sub`、`iat`、`exp` 分别表示什么。
- 知道 Token 应在 Service 登录成功后生成。
- 知道 Controller 可以通过 `Authorization: Bearer <token>` 返回 Token。
- 能写出客户端携带 Token 的请求头。
- 能理解拦截器校验 Token 的四步流程。
- 知道验证码要存入 Session，并设置过期时间。
- 知道验证码校验成功后要从 Session 中删除，避免重复使用。
