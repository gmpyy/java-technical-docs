---
title: "Redis 高级结构"
description: "Spring Bean 补充、Redis List 队列、Stream、GEO、Bitmap 与 HyperLogLog"
outline: [2, 4]
---

# Redis 高级结构

这一章对应 `JAVA.md` 末尾内容：Spring Bean 补充、基于 Redis List 的消息队列、Stream 消息队列、GEO、Bitmap 和 HyperLogLog。

## Spring Bean 补充

### 你可以把 Spring 想成一个“大工厂”

- 类：像图纸。
- 对象：像按图纸造出来的产品。
- Bean：像被 Spring 这个工厂统一生产、统一管理的产品。

Spring 不只是帮你造对象，还会帮你做这些事：

- 创建对象。
- 注入依赖。
- 控制生命周期。
- 初始化和销毁。
- 管理单例、多例等作用域。

```java
@Repository
public class UserMapper {
}

@Service
public class UserService {
    @Autowired
    private UserMapper userMapper;
}
```

这里：

- `UserMapper` 是一个 Bean。
- `UserService` 也是一个 Bean。

Spring 启动时会：

1. 创建 `UserMapper` Bean。
2. 创建 `UserService` Bean。
3. 把 `UserMapper` 注入到 `UserService` 里。

## Spring 怎么判断 Bean

Spring 主要通过这些注解判断哪些类要交给容器管理：

- `@Component`
- `@Service`
- `@Controller`
- `@Repository`

## Spring 会去扫描这些类

Spring 启动时会扫描你配置的包，看看哪些类上有这些注解。

比如主启动类：

```java
@SpringBootApplication
public class Application {
}
```

`@SpringBootApplication` 里包含组件扫描能力，默认会扫描**启动类所在包及其子包**。

如果扫描到：

```java
@Service
public class UserService {
}
```

Spring 就会把它创建出来，放进容器里，变成 Bean。

## 也可以用 `@Bean` 手动注册

除了在类上加注解，还可以在配置类里手动声明：

```java
@Configuration
public class AppConfig {

    @Bean
    public UserService userService() {
        return new UserService();
    }
}
```

这里 Spring 会把 `userService()` 方法返回的对象也注册成 Bean。

所以这也是在告诉 Spring：**这个对象归你管。**

## 基于 Redis 的 List 实现消息队列

基于 Redis List 实现消息队列只适用于简单场景。

### 优点

- 实现简单：Redis 本身就支持 List，不用额外引入 MQ 中间件。
- 性能高：Redis 基于内存，读写很快，适合轻量级异步任务。
- 支持阻塞读取：`BLPOP` / `BRPOP` 可以让消费者没消息时阻塞等待，不用一直轮询。
- 开发成本低：很多项目本来就有 Redis，直接拿来做简单队列很方便。

```bash
LPUSH queue:orders order-1
BRPOP queue:orders 30
```

### 缺点

- 可靠性一般：消费者把消息弹出后如果还没处理完就宕机，消息可能直接丢失。
- 不支持复杂确认机制：不像 RabbitMQ、Kafka 那样天然有 ack、重投、死信队列这些能力。
- 不适合大规模堆积：Redis 更适合做高性能缓存和轻量队列，不适合长期堆很多消息。
- 消费能力有限：List 更偏简单一对一 / 一对多抢消息，不擅长复杂消费组场景。
- 运维风险更高：如果 Redis 本身主要还承担缓存、锁、Session，再拿它扛大量消息，容易互相影响。

## 基于 Stream 的消息队列

Redis Stream 比 List 更适合做消息队列，因为它支持消费者组、消息确认和 Pending List。

源笔记中的关键命令：

- `XADD` 生产消息。
- `XREADGROUP` 读新消息。
- 成功后 `XACK`。
- 定时扫 Pending List。
- 用 `XAUTOCLAIM` 重领超时消息。
- 用业务唯一键做幂等。
- 超过最大重试次数进死信队列。

示例：

```bash
XADD stream.orders * userId 1 voucherId 100
XGROUP CREATE stream.orders group.orders 0 MKSTREAM
XREADGROUP GROUP group.orders consumer-1 COUNT 1 BLOCK 2000 STREAMS stream.orders >
XACK stream.orders group.orders 1700000000000-0
```

处理流程：

```text
生产者 XADD 写消息
  -> 消费者组 XREADGROUP 读取新消息
  -> 业务处理
  -> 成功后 XACK
  -> 失败或超时进入 Pending List
  -> XAUTOCLAIM 重领超时消息
  -> 超过最大重试进入死信队列
```

## GEO

GEO 就是 Redis 里专门处理“地理坐标”的能力，本质上是拿经纬度做存储、距离计算和附近搜索。

典型场景：

- 保存商户坐标。
- 查找附近门店。
- 计算两个地点距离。
- 按距离排序。

```bash
GEOADD shop:geo 116.397128 39.916527 shop:1
GEOADD shop:geo 121.473701 31.230416 shop:2
GEODIST shop:geo shop:1 shop:2 km
GEOSEARCH shop:geo FROMLONLAT 116.39 39.91 BYRADIUS 5 km WITHDIST
```

## Bitmap

Bitmap 就是用一个 bit 位表示一个状态的数据结构。

在签到场景里，可以用每一位表示某一天是否签到：

- 签到了是 `1`
- 没签到是 `0`

一个字符串可以代表一个月的签到情况。

```bash
SETBIT sign:1001:2026-05 0 1
SETBIT sign:1001:2026-05 1 1
GETBIT sign:1001:2026-05 0
BITCOUNT sign:1001:2026-05
```

示例理解：

```text
第 1 天签到 -> bit 0 = 1
第 2 天签到 -> bit 1 = 1
第 3 天没签 -> bit 2 = 0
```

Bitmap 非常适合“是否”类状态，比如签到、是否活跃、是否访问过。

## HyperLogLog 实现 UV 统计

UV 统计的难点是“去重还不能太占内存”。Redis 的 HyperLogLog 用“允许极小误差换超低内存”的方式，专门解决这种海量去重计数问题。

一个最贴近视频的例子：

- 今天访问网站的用户有很多，用户 A 来了 10 次。
- 对 PV 来说，这 10 次都算。
- 对 UV 来说，只能算 1 次。
- 如果你把所有来过的人都记下来，太占内存。
- 所以用 `PFADD uv:2026-04-19 userId` 记访问过的人。
- 再用 `PFCOUNT uv:2026-04-19` 估算今天 UV。
- 如果要算 4 月 UV，就把每天的 key 做 `PFMERGE`。

```bash
PFADD uv:2026-04-19 user:1
PFADD uv:2026-04-19 user:2
PFADD uv:2026-04-19 user:1

PFCOUNT uv:2026-04-19

PFMERGE uv:2026-04 uv:2026-04-18 uv:2026-04-19
PFCOUNT uv:2026-04
```

适合场景：

- 日 UV。
- 月 UV。
- 活动访问人数估算。
- 大量用户去重计数。

不适合场景：

- 需要精确名单。
- 需要精确计数。
- 需要知道具体有哪些用户访问过。

## 本章检查

- 能用“大工厂”类比解释 Spring Bean。
- 知道 `@Component`、`@Service`、`@Controller`、`@Repository` 会被扫描成 Bean。
- 知道 `@Bean` 可以手动注册对象。
- 能说出 Redis List 做消息队列的优缺点。
- 能说出 Stream 的 `XADD`、`XREADGROUP`、`XACK`、Pending List、`XAUTOCLAIM`。
- 能说明 GEO 适合附近搜索。
- 能说明 Bitmap 适合签到这类布尔状态。
- 能说明 HyperLogLog 为什么适合 UV 统计。
