---
title: "Redis 基础与登录链路"
description: "Redis 特点、五种基本数据类型、Spring Boot 配置、黑马点评短信验证码和登录拦截器"
outline: [2, 4]
---

# Redis 基础与登录链路

这一章对应 `JAVA.md` 中 Redis 开头到“更新用户信息的保存”部分。这里保留 Redis 基础特点、常用指令图、五种基本数据类型、Spring Boot 项目依赖配置图，以及黑马点评登录链路。

## Redis

### 基础特点

Redis 数据存储在内存中，一般的 SQL 数据库的数据都存储在磁盘中。存储在内存中的数据读取速度快。

Redis 的几个入门特点：

- 单线程，每个命令具备原子性。
- 持久化存储，可以定期把数据快照保存到磁盘，保证服务器重启后可以还原大部分数据。
- 适合缓存、验证码、登录态、计数、排行榜、分布式锁等场景。

### Redis 常用指令

![Redis 常用指令](/java-technical-docs/images/source/image-48.png)

常见命令示例：

```bash
SET name tom
GET name

HSET user:1 username tom age 18
HGET user:1 username

LPUSH queue a b c
RPOP queue

SADD tags java redis spring
SMEMBERS tags

ZADD rank 100 tom 90 jerry
ZRANGE rank 0 -1 WITHSCORES
```

## Redis 五种基本数据类型

### String：字符串

最简单的类型，可以存普通字符串，也可以存序列化对象，比如 JSON。

适合：

- 验证码
- token
- 计数器
- 简单缓存

```bash
SET login:code:13800000000 123456 EX 120
GET login:code:13800000000
```

### Hash：哈希

类似 MySQL 的一行或 Python 的 `dict`，适合存对象，也就是多个键值对的组合。

```bash
HSET login:token:abc123 id 1 nickName tom icon avatar.png
HGETALL login:token:abc123
```

### List：列表

有序可重复的字符串数组，插入删除 `O(1)`，两头操作快。

```bash
LPUSH queue msg1
RPOP queue
```

### Set：集合

无序不重复的字符串集合，支持查询 Set 之间的交集、并集、差集。

```bash
SADD user:1:follows 2 3 4
SADD user:2:follows 3 4 5
SINTER user:1:follows user:2:follows
```

### Sorted Set：有序集合

每个元素带分数，按分数排序，适合排行榜。

```bash
ZADD shop:rank 100 shopA 95 shopB
ZRANGE shop:rank 0 -1 WITHSCORES
```

## 创建 Spring Boot 项目并配置 Redis

在 VS Code 上创建项目时，选择 Spring Boot 创建，而不是普通 Maven。

项目信息：

- `group-id`：`com.study`
- 项目 ID：`study1`

需要的依赖：

1. `spring-boot-starter-data-redis`：Redis 数据访问
2. `commons-pool2`：Redis 连接池支持
3. `lombok`：简化代码，比如 getter / setter
4. `spring-boot-starter-data-redis-test`：测试支持，`test` scope
5. Spring Web

![Spring Boot Redis 配置 1](/java-technical-docs/images/source/image-49.png)

![Spring Boot Redis 配置 2](/java-technical-docs/images/source/image-50.png)

![Spring Boot Redis 配置 3](/java-technical-docs/images/source/image-51.png)

常见配置示例：

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379
      lettuce:
        pool:
          max-active: 8
          max-idle: 8
          min-idle: 0
```

## 黑马点评

### 实现短信验证码功能

源笔记中的主线：

1. 逻辑记得写到 Service。
2. 验证手机号。
3. 生成验证码。
4. 保存 Session。
5. 发送验证码。
6. 返回 `ok`。

如果改为 Redis 保存验证码，可以用手机号作为 key：

```java
public Result sendCode(String phone) {
    if (RegexUtils.isPhoneInvalid(phone)) {
        return Result.fail("手机号格式错误");
    }

    String code = RandomUtil.randomNumbers(6);
    stringRedisTemplate.opsForValue()
            .set("login:code:" + phone, code, Duration.ofMinutes(2));

    // 真实项目中这里调用短信平台
    log.debug("发送短信验证码成功，验证码：{}", code);
    return Result.ok();
}
```

### 登录接口

源笔记中的登录步骤：

1. 接收 `phone` 和 `code` 参数。
2. 校验手机号格式。
3. 从 Session 获取保存的验证码并比对。
4. 验证成功后删除 Session 中的验证码。
5. 根据手机号查询用户，不存在则创建新用户。
6. 将用户信息保存到 Session。
7. 返回成功。

改造为 Redis 后，典型流程是：

1. 接收 `phone` 和 `code`。
2. 从 Redis 取 `login:code:{phone}`。
3. 对比验证码。
4. 查询或创建用户。
5. 生成 token。
6. 用 token 作为 key，把用户信息保存到 Redis。
7. token 返回给前端。

```java
public Result login(LoginFormDTO loginForm) {
    String phone = loginForm.getPhone();

    if (RegexUtils.isPhoneInvalid(phone)) {
        return Result.fail("手机号格式错误");
    }

    String cacheCode = stringRedisTemplate.opsForValue().get("login:code:" + phone);
    String code = loginForm.getCode();

    if (cacheCode == null || !cacheCode.equals(code)) {
        return Result.fail("验证码错误");
    }

    User user = queryOrCreateUser(phone);
    String token = UUID.randomUUID().toString(true);

    UserDTO userDTO = BeanUtil.copyProperties(user, UserDTO.class);
    Map<String, Object> userMap = BeanUtil.beanToMap(userDTO);

    stringRedisTemplate.opsForHash().putAll("login:token:" + token, userMap);
    stringRedisTemplate.expire("login:token:" + token, Duration.ofMinutes(30));

    return Result.ok(token);
}
```

### 登录拦截器

源笔记中的登录拦截器流程：

1. 请求进入拦截器。
2. 从 Session 获取 `user`。
3. 如果没有 `user`，返回 401 拦截。
4. 如果有 `user`，保存到 `ThreadLocal` 中的 `UserHolder`，放行。
5. Controller 中的 `me` 接口从 `UserHolder` 获取用户。
6. 请求完成后在 `afterCompletion` 中清理 `UserHolder`。

`ThreadLocal` 的作用：比如在拦截器里保存了用户信息，那么在这个请求中，就可以直接从 `ThreadLocal` 获取用户信息，不需要每个接口都从 Session 中获取。这个保存操作通常在拦截器进行，这样每个接口经过拦截器后都可以获取到需要的信息，比如用户信息。

改成 Redis token 后的拦截器思路：

```java
public boolean preHandle(HttpServletRequest request,
                         HttpServletResponse response,
                         Object handler) {
    String token = request.getHeader("authorization");
    if (StrUtil.isBlank(token)) {
        return true;
    }

    String tokenKey = "login:token:" + token;
    Map<Object, Object> userMap = stringRedisTemplate.opsForHash().entries(tokenKey);

    if (userMap.isEmpty()) {
        return true;
    }

    UserDTO userDTO = BeanUtil.fillBeanWithMap(userMap, new UserDTO(), false);
    UserHolder.saveUser(userDTO);

    stringRedisTemplate.expire(tokenKey, Duration.ofMinutes(30));
    return true;
}

public void afterCompletion(HttpServletRequest request,
                            HttpServletResponse response,
                            Object handler,
                            Exception ex) {
    UserHolder.removeUser();
}
```

### 集群问题

Session 存在集群共享问题：多台服务器无法共享 Session，因此比 Session 更好的方案就是 Redis。

```text
客户端
  -> Nginx
  -> App-1 / App-2 / App-3
  -> Redis 共享验证码和登录态
```

### 更新验证码的保存

用手机号作为 key，保存到 Redis。

```text
login:code:{phone} -> code
```

示例：

```java
stringRedisTemplate.opsForValue()
        .set("login:code:" + phone, code, Duration.ofMinutes(2));
```

### 更新用户信息的保存

源笔记中的改造点：

- token 作为 key 保存用户信息。
- token 保存到请求头。
- 每次请求经过拦截器都会刷新 token 的时间。

```text
login:token:{token} -> user hash
```

示例：

```java
stringRedisTemplate.opsForHash().putAll("login:token:" + token, userMap);
stringRedisTemplate.expire("login:token:" + token, Duration.ofMinutes(30));
```

## 本章检查

- 能说出 Redis 为什么快。
- 能说出 Redis 单线程和单命令原子性的含义。
- 能区分 String、Hash、List、Set、Sorted Set。
- 知道 Spring Boot 配置 Redis 需要哪些依赖。
- 能描述短信验证码发送和登录流程。
- 知道 Session 在集群下的问题。
- 能说清验证码用手机号做 key、用户信息用 token 做 key 的 Redis 登录改造方式。
- 知道请求结束后要清理 `ThreadLocal`。
