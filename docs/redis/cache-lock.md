---
title: "缓存、锁与秒杀"
description: "Redis 缓存、缓存穿透/击穿、逻辑过期、乐观锁、同步锁、分布式锁、Redisson 与异步秒杀"
outline: [2, 4]
---

# 缓存、锁与秒杀

这一章对应 `JAVA.md` 中 Redis 缓存、缓存问题、秒杀并发、分布式锁和 Redisson 部分。这里保留源笔记的流程、注意点和相关图片。

## 更新用户信息的保存

在 Redis 登录改造中，用户信息保存方式是：

- token 作为 key 保存用户信息。
- token 保存到请求头。
- 每次请求经过拦截器都会刷新 token 的时间。

```text
login:token:{token} -> user hash
```

## 给特定接口添加 Redis 缓存

给商铺查询这类接口添加 Redis 缓存的流程：

1. 查询商铺时，先从 Redis 缓存查找。
2. 缓存命中则直接返回。
3. 缓存未命中则查数据库。
4. 查询结果写入 Redis 缓存。
5. 返回商铺信息。

```java
public Shop queryById(Long id) {
    String key = "cache:shop:" + id;
    String json = stringRedisTemplate.opsForValue().get(key);

    if (StrUtil.isNotBlank(json)) {
        return JSONUtil.toBean(json, Shop.class);
    }

    Shop shop = getById(id);
    if (shop == null) {
        return null;
    }

    stringRedisTemplate.opsForValue()
            .set(key, JSONUtil.toJsonStr(shop), Duration.ofMinutes(30));
    return shop;
}
```

## 缓存更新最佳实践

![缓存更新最佳实践](/java-technical-docs/images/source/image-52.png)

常见策略：

- 先更新数据库，再删除缓存。
- 给缓存设置过期时间作为兜底。
- 对一致性要求非常高时，引入消息队列、binlog 订阅或延迟双删等方案。

```text
更新数据
  -> 写数据库
  -> 删除缓存
  -> 下次查询时重建缓存
```

## 缓存穿透

缓存穿透：查询一个不存在的数据，比如 `id = -1`，Redis 没有，数据库也没有。每次请求都会打到数据库。

解决方式：当数据库也查不到时，往 Redis 写入一个空值 `""`，设置较短 TTL，比如 2 分钟。这样下次查询同样不存在的数据时，直接从 Redis 返回空值，不用查数据库。

```java
Shop shop = getById(id);
if (shop == null) {
    stringRedisTemplate.opsForValue()
            .set("cache:shop:" + id, "", Duration.ofMinutes(2));
    return null;
}
```

补充方案：

- 做参数合法性校验。
- 使用布隆过滤器过滤明显不存在的 key。

## 互斥锁防止缓存击穿

缓存击穿：热点 key 过期后，大量请求同时访问数据库。

互斥锁流程：

```text
请求1 ──┐
请求2 ──┼──> 查 Redis 缓存未命中 ──> 抢锁
请求3 ──┘                              │

抢到   ──> 查 DB ──> 写缓存 ──> 释放锁
没抢到 ──> 休眠 50ms ──> 重试查缓存
```

实际实现可以用 Redis 自带的 `setIfAbsent` 来实现互斥锁效果。

```java
private boolean tryLock(String key) {
    Boolean flag = stringRedisTemplate.opsForValue()
            .setIfAbsent(key, "1", Duration.ofSeconds(10));
    return Boolean.TRUE.equals(flag);
}

private void unlock(String key) {
    stringRedisTemplate.delete(key);
}
```

## 逻辑过期策略防范缓存击穿

逻辑过期策略不会让热点数据直接从 Redis 消失，而是在数据里额外保存一个逻辑过期时间。

流程：

```text
请求1 ──┐
请求2 ──┼──> 查 Redis ──> 数据已逻辑过期 ──> 抢锁
请求3 ──┘                              │

抢到   ──> 开启新线程重建缓存 ──> 返回旧数据
没抢到 ──> 直接返回旧数据
```

适用场景：

- 热点数据。
- 读多写少。
- 可以短时间接受旧数据。

```java
public class RedisData {
    private LocalDateTime expireTime;
    private Object data;
}
```

## 缓存的封装方法

![缓存封装方法](/java-technical-docs/images/source/image-53.png)

封装缓存工具类时，可以把下面几类能力抽出来：

- 普通缓存查询。
- 缓存空值防穿透。
- 互斥锁重建缓存。
- 逻辑过期重建缓存。

## 使用乐观锁解决超卖问题

源笔记中的流程：

1. **分析问题**：发现原有代码先查后改，在高并发下存在非原子操作导致超卖。
2. **编写 CAS Lua 脚本**：实现版本号比对和扣减的原子操作。
3. **查询库存作为版本号**：先用 `GET` 获取当前库存值。
4. **传入版本号执行扣减**：用 `execute(SECKILL_SCRIPT, keys, version)` 执行。
5. **处理结果**：判断返回值，`-1` 表示版本号不匹配，被其他线程修改过；其他值表示扣减后剩余库存。

注意：这种方法在高并发场景下，很多请求都会因为版本号不一致而失败。所以在数量少、高并发场景下往往不是一个好的解决方案。这个解决方案更适合库存充足的场景。

更常见的数据库乐观扣减方式：

```sql
UPDATE voucher
SET stock = stock - 1
WHERE id = #{voucherId}
  AND stock > 0;
```

Redis Lua 原子扣减思路：

```lua
local stock = tonumber(redis.call('GET', KEYS[1]))
if stock == nil or stock <= 0 then
  return -1
end
redis.call('DECR', KEYS[1])
return stock - 1
```

## 同步锁和事务解决一人一单问题

`synchronized` 同步锁：

- 作用：保证同一时刻只有一个线程能执行这段代码。

`@Transactional` 事务：

- 作用：保证一系列操作要么全部成功，要么全部失败回滚。

注意：事务的提交会在方法执行完之后由 Spring 提交，这段提交时间可能比较长。

解决思路：

1. 用户发起秒杀请求。
2. 查询秒杀券信息。
3. 判断秒杀时间是否有效。
4. Lua 脚本扣减库存，保证原子操作。
5. 进入 `createVoucherOrder` 方法。
6. `synchronized` 锁定用户，相同用户串行，不同用户并行。
7. 事务内检查一人一单。
   - 如果已购买，归还库存，返回失败。
   - 如果未购买，创建订单，返回成功。
8. 释放锁。

为什么要先锁住再进入事务逻辑：如果先执行事务，里面的逻辑执行完之后，事务还没提交的间隙，锁已经释放。此时如果同一用户还有请求进来，由于事务还没提交，查询到仍然是未购买，就会再次执行事务里的逻辑，导致一人多单问题。

```java
Long userId = UserHolder.getUser().getId();
synchronized (userId.toString().intern()) {
    return createVoucherOrder(voucherId);
}
```

## 分布式锁

利用同步锁加事务可以解决单进程状态下的一人一单问题。但是对于集群，会有多个进程，每个进程都有不同的锁监听器。同步锁在集群状态下就没有效果，因为同步锁只能对它所在的进程生效，其他进程不会共用同一个同步锁。这时候就需要多个进程共同的锁，也就是分布式锁。

![分布式锁原理](/java-technical-docs/images/source/image-54.png)

定义一个类实现分布式锁：

![自定义分布式锁](/java-technical-docs/images/source/image-55.png)

优化分布式锁，防止释放别人的锁：

![防止释放别人的锁](/java-technical-docs/images/source/image-56.png)

基础加锁：

```java
Boolean success = stringRedisTemplate.opsForValue()
        .setIfAbsent("lock:order:" + userId, threadId, Duration.ofSeconds(10));
```

优化分布式锁 step 2：使用 Lua 脚本保证“判断一致”和“释放锁”是一个原子操作，防止判断之后、释放之前又有别的线程使用分布式锁，导致最后释放的是别的线程的锁。

```lua
if redis.call('get', KEYS[1]) == ARGV[1] then
  return redis.call('del', KEYS[1])
end
return 0
```

## Redisson

Redisson 是基于 Redis 实现的分布式组件库，里面也包括分布式锁。

它解决了分布式锁的多种问题：

- **可重入**：同一个线程再次获取这把锁时不会被阻塞，而是根据线程标识判断为当前持锁线程，并将锁的重入次数加一。
- **可重试**：线程获取锁失败后不会立即结束，而是通过订阅锁释放消息，在锁释放后被唤醒并再次竞争锁。
- **防止超时释放**：线程持有锁期间，看门狗会定时为锁续期，只要业务还没执行完，锁就不会因为超时自动释放。
- **主从一致性问题**：为避免锁刚写入主节点但还没同步就发生主从切换，可以使用联合锁，在多个独立 Redis 节点上同时加锁，只有都成功才算真正加锁成功，从而降低锁丢失风险。

示例：

```java
RLock lock = redissonClient.getLock("lock:order:" + userId);
boolean isLock = lock.tryLock();

try {
    if (!isLock) {
        return Result.fail("不允许重复下单");
    }
    return createVoucherOrder(voucherId);
} finally {
    if (isLock) {
        lock.unlock();
    }
}
```

## 基于阻塞队列的异步秒杀优化

实现思路：

1. 利用 Redis 判断库存余量以及确保一人一单，直接返回订单信息。
2. 下单业务放入阻塞队列，利用子线程异步下单。

涉及组件：

- 阻塞队列：`BlockingQueue`
- 线程池：`ExecutorService`
- `@PostConstruct`：确保初始化立即执行，类似 Vue 的 `onMounted`

```java
private final BlockingQueue<VoucherOrder> orderTasks = new ArrayBlockingQueue<>(1024 * 1024);
private static final ExecutorService SECKILL_ORDER_EXECUTOR = Executors.newSingleThreadExecutor();

@PostConstruct
private void init() {
    SECKILL_ORDER_EXECUTOR.submit(new VoucherOrderHandler());
}
```

存在缺陷：

- 内存有限，阻塞队列长度有限。
- 服务重启可能丢失内存队列中的任务。
- 更可靠的方案可以把队列放到 MQ 或 Redis Stream 中。

## Spring Bean 生命周期补充

一个 Spring Bean 大致经历这样几个阶段：

1. Spring 创建对象。
2. Spring 给它注入依赖。
3. 执行 `@PostConstruct`。
4. 这个 Bean 才算真正可用。

Bean 可以简单理解成：**交给 Spring 容器管理的对象。**

## 本章检查

- 能给查询接口加 Redis 缓存。
- 能说出缓存穿透和缓存击穿的区别。
- 能解释缓存空值、互斥锁、逻辑过期分别解决什么问题。
- 能说明乐观锁为什么在高并发少库存时失败率高。
- 能解释为什么本地同步锁不适合多实例集群。
- 能说出分布式锁释放时为什么要先校验锁标识。
- 能说明 Redisson 的可重入、可重试、看门狗续期。
- 能描述基于阻塞队列的异步秒杀流程和缺陷。
