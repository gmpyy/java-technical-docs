---
title: "缓存、锁与秒杀"
description: "缓存更新、缓存穿透、缓存击穿、逻辑过期、乐观锁、分布式锁、Redisson 与异步秒杀"
outline: [2, 3]
---

# 缓存、锁与秒杀

Redis 在高并发场景下最常见的用法是缓存和锁。缓存解决读压力，锁解决并发写冲突，但两者都需要处理失败和边界条件。

## 给接口添加 Redis 缓存

缓存查询的一般模式：

```text
查 Redis
  -> 命中：返回
  -> 未命中：查数据库
      -> 数据存在：写 Redis，返回
      -> 数据不存在：缓存空值，返回
```

```java
public Shop queryById(Long id) {
    String key = "cache:shop:" + id;
    String json = stringRedisTemplate.opsForValue().get(key);
    if (StrUtil.isNotBlank(json)) {
        return JSONUtil.toBean(json, Shop.class);
    }
    if (json != null) {
        return null;
    }

    Shop shop = getById(id);
    if (shop == null) {
        stringRedisTemplate.opsForValue().set(key, "", Duration.ofMinutes(2));
        return null;
    }
    stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop), Duration.ofMinutes(30));
    return shop;
}
```

## 缓存更新最佳实践

常见策略：

- 先更新数据库，再删除缓存。
- 缓存设置过期时间兜底。
- 对一致性要求极高时，引入消息队列或订阅 binlog。

```text
更新数据库
  -> 删除缓存
  -> 下次读取时重建缓存
```

## 缓存穿透

缓存穿透是指查询数据库也不存在的数据，导致请求每次都打到数据库。

解决方法：

- 缓存空值，设置较短 TTL。
- 使用布隆过滤器过滤不存在的 key。
- 做参数合法性校验。

## 缓存击穿

缓存击穿是热点 key 过期后，大量请求同时访问数据库。

## 互斥锁防止缓存击穿

```text
请求进来
  -> 查缓存未命中
  -> 抢锁
      -> 抢到：查数据库，写缓存，释放锁
      -> 没抢到：短暂休眠后重试查缓存
```

```java
private boolean tryLock(String key) {
    Boolean success = stringRedisTemplate.opsForValue()
            .setIfAbsent(key, "1", Duration.ofSeconds(10));
    return Boolean.TRUE.equals(success);
}

private void unlock(String key) {
    stringRedisTemplate.delete(key);
}
```

## 逻辑过期策略

逻辑过期不会让热点数据直接从 Redis 消失，而是在数据里保存一个过期时间。过期后先返回旧值，再异步重建缓存。

```java
public class RedisData {
    private LocalDateTime expireTime;
    private Object data;
}
```

适合读多写少、允许短时间旧数据的热点场景。

## 使用乐观锁解决超卖问题

秒杀扣库存要保证原子性，可以使用版本号、CAS 或 Lua 脚本。

```sql
UPDATE voucher
SET stock = stock - 1
WHERE id = ? AND stock > 0;
```

如果更新行数为 0，说明库存不足或并发竞争失败。

## 同步锁和事务解决一人一单

一人一单需要同时保证：

- 同一个用户不能重复下单。
- 扣库存和创建订单要在事务中完成。

```java
@Transactional
public void createVoucherOrder(Long voucherId) {
    Long userId = UserHolder.getUser().getId();
    synchronized (userId.toString().intern()) {
        int count = query().eq("user_id", userId).eq("voucher_id", voucherId).count();
        if (count > 0) {
            throw new BusinessException("不能重复下单");
        }
        save(new VoucherOrder(userId, voucherId));
    }
}
```

::: warning 注意
本地 `synchronized` 只能保护单 JVM。多实例部署时，需要分布式锁。
:::

## 分布式锁

Redis 分布式锁常用 `SET key value NX EX seconds`，释放锁前必须校验锁标识，防止释放别人的锁。

```java
String lockValue = UUID.randomUUID().toString();
Boolean success = stringRedisTemplate.opsForValue()
        .setIfAbsent("lock:order:" + userId, lockValue, Duration.ofSeconds(10));
```

释放锁要用 Lua 保证“判断 + 删除”原子执行。

```lua
if redis.call('get', KEYS[1]) == ARGV[1] then
  return redis.call('del', KEYS[1])
end
return 0
```

## Redisson

Redisson 是基于 Redis 的分布式组件库，封装了分布式锁、可重入锁、看门狗续期等能力。

```java
RLock lock = redissonClient.getLock("lock:order:" + userId);
boolean locked = lock.tryLock();
try {
    if (!locked) {
        throw new BusinessException("请勿重复下单");
    }
    createOrder();
} finally {
    if (locked) {
        lock.unlock();
    }
}
```

## 基于阻塞队列的异步秒杀优化

高并发秒杀可以先在 Redis 中完成库存判断和一人一单校验，再把订单消息放入阻塞队列，由后台线程异步写数据库。

```text
请求线程
  -> Redis Lua 判断库存和一人一单
  -> 返回订单 ID
  -> 订单消息进入 BlockingQueue

后台线程
  -> 从队列取订单
  -> 开启事务写数据库
```

```java
private final BlockingQueue<VoucherOrder> orderTasks = new ArrayBlockingQueue<>(1024 * 1024);
private final ExecutorService executor = Executors.newSingleThreadExecutor();
```

