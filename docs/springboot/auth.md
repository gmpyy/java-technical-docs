---
title: "JWT 与验证码认证"
description: "JWT 登录流程、Token 生成和校验、Session 验证码与登录拦截器"
outline: [2, 3]
---

# JWT 与验证码认证

认证链路的核心是：登录成功后生成凭证，客户端后续请求携带凭证，服务端校验凭证并还原用户身份。

## JWT 登录阶段

登录成功后，服务端生成 JWT。常见字段包括：

| 字段 | 含义 |
| --- | --- |
| `iat` | Issued At，签发时间 |
| `exp` | Expiration，过期时间 |
| `sub` / `userId` | 用户标识 |

```java
public class JwtUtil {
    public String createToken(Long userId) {
        Date now = new Date();
        Date expire = new Date(now.getTime() + 2 * 60 * 60 * 1000);

        return Jwts.builder()
                .setSubject(String.valueOf(userId))
                .setIssuedAt(now)
                .setExpiration(expire)
                .signWith(secretKey)
                .compact();
    }
}
```

## AuthService 登录

```java
@Service
public class AuthService {
    public String login(LoginDTO dto) {
        UserEntity user = userMapper.findByPhone(dto.getPhone());
        if (user == null) {
            throw new BusinessException("用户不存在");
        }
        return jwtUtil.createToken(user.getId());
    }
}
```

## AuthController 返回 Token

```java
@RestController
@RequestMapping("/api/auth")
public class AuthController {
    @PostMapping("/login")
    public LoginVO login(@RequestBody LoginDTO dto) {
        String token = authService.login(dto);
        return new LoginVO(token);
    }
}
```

客户端请求时携带：

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

## 服务端校验 Token

```java
public class JwtAuthInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) throws Exception {
        String authorization = request.getHeader("Authorization");
        if (authorization == null || !authorization.startsWith("Bearer ")) {
            response.setStatus(401);
            return false;
        }

        String token = authorization.substring(7);
        Long userId = jwtUtil.parseUserId(token);
        UserHolder.save(userId);
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler,
                                Exception ex) {
        UserHolder.remove();
    }
}
```

## Session 验证码

验证码流程：

1. 生成随机验证码。
2. 生成图片或 Base64。
3. 写入 Session。
4. 登录时读取 Session 并对比。
5. 校验成功后删除验证码。

```java
@PostMapping("/captcha")
public CaptchaVO captcha(HttpSession session) {
    String code = captchaUtil.randomCode();
    session.setAttribute("captcha", code);
    String image = captchaUtil.base64Image(code);
    return new CaptchaVO(image, 120);
}
```

## 登录时校验验证码

```java
public void checkCaptcha(HttpSession session, String input) {
    String saved = (String) session.getAttribute("captcha");
    if (saved == null) {
        throw new BusinessException("验证码已过期");
    }
    if (!saved.equalsIgnoreCase(input)) {
        throw new BusinessException("验证码错误");
    }
    session.removeAttribute("captcha");
}
```

::: tip 快速检查
Token 校验通过后保存用户上下文，请求完成后必须清理 `ThreadLocal`。
:::

