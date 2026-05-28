---
title: "Redis 基础与登录链路"
description: "Redis 特点、五种基本数据类型、短信验证码、登录接口、登录拦截器与集群问题"
outline: [2, 3]
---

# Redis 基础与登录链路

Redis 常用于缓存、验证码、登录态、分布式锁、消息队列和统计计数。它的优势是读写快，单个命令具备原子性。

## 基础特点

- 单线程执行命令，单个命令具备原子性。
- 支持持久化，可以把数据快照或追加日志保存到磁盘。
- 适合高频读写、短期状态、缓存和简单并发控制。

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379
      lettuce:
        pool:
          max-active: 8
```

常见依赖：

- `spring-boot-starter-data-redis`
- `commons-pool2`
- `lombok`

## Redis 五种基本数据类型

| 类型 | 适合数据 | 常见命令 |
| --- | --- | --- |
| String | 字符串、数字、JSON | `GET`、`SET`、`INCR` |
| Hash | 对象字段 | `HGET`、`HSET` |
| List | 有序列表 | `LPUSH`、`RPOP` |
| Set | 去重集合 | `SADD`、`SISMEMBER` |
| Sorted Set | 排行榜、权重排序 | `ZADD`、`ZRANGE` |

```shell
SET user:1:name tom
GET user:1:name
HSET user:1 phone 13800000000 nickname tom
SADD tags java redis spring
```

## 黑马点评：短信验证码功能

短信验证码主流程：

1. 校验手机号格式。
2. 生成验证码。
3. 保存验证码。
4. 发送验证码。
5. 返回结果。

```java
public Result sendCode(String phone) {
    if (!RegexUtils.isPhoneInvalid(phone)) {
        return Result.fail("手机号格式错误");
    }
    String code = RandomUtil.randomNumbers(6);
    stringRedisTemplate.opsForValue()
            .set("login:code:" + phone, code, Duration.ofMinutes(2));
    return Result.ok();
}
```

## 登录接口

登录接口通常要做：

- 接收 `phone` 和 `code`。
- 校验手机号格式。
- 从 Redis 获取保存的验证码并对比。
- 验证成功后删除验证码或让它自然过期。
- 查询用户，不存在则创建用户。
- 保存用户登录态。

```java
public Result login(LoginFormDTO loginForm) {
    String phone = loginForm.getPhone();
    String cacheCode = stringRedisTemplate.opsForValue().get("login:code:" + phone);
    if (!loginForm.getCode().equals(cacheCode)) {
        return Result.fail("验证码错误");
    }
    User user = queryOrCreateUser(phone);
    String token = UUID.randomUUID().toString(true);
    saveUserToRedis(token, user);
    return Result.ok(token);
}
```

## 登录拦截器

登录拦截器主线：

1. 请求进入拦截器。
2. 从请求头读取 token。
3. 根据 token 从 Redis 读取用户。
4. 没有用户则返回 401 或放行到需要登录的拦截器处理。
5. 有用户则保存到 `UserHolder`。
6. 请求完成后清理 `UserHolder`。

```java
public boolean preHandle(HttpServletRequest request,
                         HttpServletResponse response,
                         Object handler) {
    String token = request.getHeader("authorization");
    if (StrUtil.isBlank(token)) {
        return true;
    }
    Map<Object, Object> userMap = stringRedisTemplate.opsForHash()
            .entries("login:token:" + token);
    if (userMap.isEmpty()) {
        return true;
    }
    UserHolder.saveUser(BeanUtil.fillBeanWithMap(userMap, new UserDTO(), false));
    return true;
}
```

## 集群问题

如果验证码和登录态保存在 Session 中，集群环境下会遇到多台服务器 Session 不共享的问题。使用 Redis 保存验证码和用户信息，可以让多台应用服务器共享登录状态。

```text
Client
  -> Nginx
  -> App 1 / App 2 / App 3
  -> Redis 保存验证码和登录态
```

