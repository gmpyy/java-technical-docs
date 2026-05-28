---
title: "Redis 高级结构"
description: "基于 List 的消息队列、Stream、GEO、Bitmap 与 HyperLogLog"
outline: [2, 3]
---

# Redis 高级结构

除了缓存和锁，Redis 还提供了 List、Stream、GEO、Bitmap、HyperLogLog 等结构，用来解决轻量队列、地理位置、签到和 UV 统计问题。

## 基于 List 的消息队列

List 可以用 `LPUSH` + `BRPOP` 实现简单消息队列。

```shell
LPUSH queue:orders order-1
BRPOP queue:orders 30
```

优点：

- 简单，容易理解。
- 适合低复杂度场景。

缺点：

- 缺少消费者组。
- 消息确认、重试、堆积治理能力弱。
- 不适合复杂可靠消息场景。

## 基于 Stream 的消息队列

Stream 是 Redis 提供的更完整的消息结构，支持消息 ID、消费者组和确认机制。

```shell
XADD stream.orders * userId 1 voucherId 100
XGROUP CREATE stream.orders group.orders 0 MKSTREAM
XREADGROUP GROUP group.orders consumer-1 COUNT 1 BLOCK 2000 STREAMS stream.orders >
XACK stream.orders group.orders 1700000000000-0
```

处理流程：

```text
XADD 生产消息
  -> XREADGROUP 消费组读取新消息
  -> 业务处理成功
  -> XACK 确认消息
```

::: tip 建议
如果只是简单队列，List 可以胜任；如果需要消费者组、确认和 pending list，优先考虑 Stream。
:::

## GEO

GEO 适合保存地理位置并按距离查询。

```shell
GEOADD shop:geo 116.397128 39.916527 shop-1
GEODIST shop:geo shop-1 shop-2 km
GEOSEARCH shop:geo FROMLONLAT 116.39 39.91 BYRADIUS 5 km WITHDIST
```

典型场景：

- 查找附近门店。
- 按距离排序。
- 保存商户坐标。

## Bitmap

Bitmap 适合保存大量布尔状态，例如用户签到。

```shell
SETBIT sign:1001:2026-05 0 1
GETBIT sign:1001:2026-05 0
BITCOUNT sign:1001:2026-05
```

如果一个用户一个月每天是否签到只需要 0/1 表示，Bitmap 会比保存一堆字符串更省空间。

## HyperLogLog

HyperLogLog 用于估算 UV，优点是占用内存很小，缺点是结果是估算值。

```shell
PFADD uv:2026-04-19 user-1 user-2 user-3
PFCOUNT uv:2026-04-19
PFMERGE uv:2026-04 uv:2026-04-18 uv:2026-04-19
```

适合场景：

- 日 UV。
- 月 UV。
- 大量用户访问去重统计。

不适合场景：

- 需要精确名单。
- 需要精确计数。
- 需要知道具体有哪些用户访问过。

## Spring Bean 创建补充

原笔记最后还提到 Spring 容器创建对象的过程，可以和 Redis 项目实践放在一起理解：

```text
Spring 扫描类
  -> 创建 Bean
  -> 注入依赖
  -> 执行 @PostConstruct
  -> Bean 可用
```

```java
@Repository
public class UserMapper {
}

@Service
public class UserService {
    private final UserMapper userMapper;

    public UserService(UserMapper userMapper) {
        this.userMapper = userMapper;
    }
}
```

