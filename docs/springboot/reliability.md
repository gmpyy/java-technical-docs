---
title: "事务与定时任务"
description: "@Transactional 事务回滚、@Scheduled 定时任务与排坑 checklist"
outline: [2, 4]
---

# 事务与定时任务

这一章对应 `JAVA.md` 中“transactional 事务”和“定时任务 scheduled”两部分。这里保留原笔记中的下单示例、事务误区、定时能力开启、三种写法、为什么定时不触发和排查清单。

## transactional 事务

### 如果没有事务，会发生什么？

假设一个典型下单流程包含三个步骤：

1. **扣库存**：库存表 `-1`
2. **扣余额**：账户表 `-金额`
3. **生成订单**：订单表 `+1`

如果这三步是独立执行的，一旦中间某一步失败，就会产生数据不一致。

例子：

- 库存已经扣了。
- 余额也扣了。
- 但在写订单时数据库报错。

最终结果：**用户钱没了、库存少了，但订单不存在**。

这就是典型的“半成功”问题。

```text
扣库存成功
  -> 扣余额成功
  -> 写订单失败
  -> 没有事务时，前两步不会自动撤销
```

### 使用 `@Transactional` 之后

`@Transactional` 的作用可以简单理解为：

> 把多个数据库操作绑定成“一次性成功 / 一次性失败”的整体。

如果方法中任何一步出现异常：

- 事务自动回滚。
- 已经执行的数据库操作都会被撤销。
- 数据恢复到操作前的状态。

这样就能保证“要么全成功，要么全失败”，避免数据不一致。

### 实际示例：简化版 Service

下面是一个典型的“下单服务”示例：

```java
@Service
public class OrderService {

    @Transactional
    public void createOrder(Long userId, Long productId, BigDecimal amount) {
        // 1. 扣库存
        inventoryRepository.decrease(productId, 1);

        // 2. 扣余额
        accountRepository.decreaseBalance(userId, amount);

        // 3. 写订单
        orderRepository.insertOrder(userId, productId, amount);

        // 如果这里抛出异常，上面所有数据库操作都会回滚
    }
}
```

运行效果：

- 三步都成功：事务提交。
- 任意一步失败：全部回滚。

### 常见误区

#### 事务只对数据库操作生效

网络请求、文件读写、已经发送出去的消息，不在数据库事务控制范围内。

```text
数据库 insert 可以回滚
HTTP 请求不能自动撤销
已经写出的文件不能自动恢复
已经发出的 MQ 消息也不能简单回滚
```

#### 默认只对运行时异常回滚

如果抛出受检异常（checked exception），默认不会回滚。

需要显式配置：

```java
@Transactional(rollbackFor = Exception.class)
public void importData() throws Exception {
    // ...
}
```

#### 自调用事务会失效

同一个类内部方法调用不会触发 Spring 事务代理，事务注解可能不生效。

```java
@Service
public class UserService {

    public void outer() {
        // 同类内部调用，可能绕过代理
        inner();
    }

    @Transactional
    public void inner() {
        // 事务可能不生效
    }
}
```

### 总结：记忆版

一句话：

`@Transactional` 是为了保证多个数据库操作要么全部成功，要么全部失败。

三条记忆点：

1. 事务的核心是“原子性”。
2. 出现异常就回滚，避免半成功。
3. 事务只管数据库，不管外部操作。

## 定时任务 scheduled

### 最小可用概念

定时任务用于让某段代码按照固定时间规则自动执行。

### 必须开启定时能力

没有开启调度功能，定时任务不会触发。

```java
@Configuration
@EnableScheduling
public class ScheduleConfig {
}
```

也可以直接写在启动类上：

```java
@EnableScheduling
@SpringBootApplication
public class StudyApplication {
    public static void main(String[] args) {
        SpringApplication.run(StudyApplication.class, args);
    }
}
```

### 三种最常见写法

- `cron`：最灵活，适合固定时间点。
- `fixedRate`：每隔固定时间执行一次，不等上一次结束。
- `fixedDelay`：上一次执行结束后再等固定时间。

```java
@Component
public class DemoJob {

    @Scheduled(cron = "*/5 * * * * *")
    public void cronJob() {
        System.out.println("cron run");
    }

    @Scheduled(fixedRate = 5000)
    public void fixedRateJob() {
        System.out.println("fixedRate run");
    }

    @Scheduled(fixedDelay = 5000)
    public void fixedDelayJob() {
        System.out.println("fixedDelay run");
    }
}
```

### 最小示例：每 5 秒执行一次

```java
@Component
public class DemoJob {

    @Scheduled(cron = "*/5 * * * * *")
    public void hello() {
        System.out.println("run scheduled job");
    }
}
```

说明：`*/5 * * * * *` 表示“每 5 秒执行一次”。

## 主线问题：为什么定时不触发？

下面是初学者最容易遇到的“定时不触发”问题，从高频到低频排列。

### 没开启 `@EnableScheduling`

症状：项目启动正常，但定时任务完全不执行。

原因：没有开启调度功能。

修复：在配置类上加 `@EnableScheduling`。

### 方法不是 `public`

症状：定时任务没有触发，但代码没报错。

原因：Spring 只会对 `public` 的方法进行调度。

修复：把定时方法改为 `public`。

### 方法有参数或返回值

症状：任务不触发，或启动时没有明显报错。

原因：`@Scheduled` 只能用于**无参数、无返回值**的方法。

修复：改成 `public void` 且无参数。

```java
@Scheduled(cron = "*/5 * * * * *")
public void run() {
    // 正确：public void，无参数
}
```

### 同类内部调用：自调用

症状：你手动调用方法时能执行，但定时任务不触发。

原因：`@Scheduled` 依赖 Spring 的代理机制，**类内部自调用会绕过代理**。

修复：确保方法由 Spring 容器调度，不要在同一个类里自己调用。

### 任务异常导致停止

症状：只执行一次，之后不再触发。

原因：任务内部抛出了异常，调度线程被中断。

修复：捕获异常并记录日志，避免任务线程死亡。

```java
@Scheduled(cron = "*/10 * * * * *")
public void safeJob() {
    try {
        // 业务逻辑
    } catch (Exception ex) {
        log.error("scheduled job failed", ex);
    }
}
```

### 时区导致“时间对不上”

症状：cron 写的是 8 点执行，但实际不是 8 点触发。

原因：默认时区和你理解的时区不同。

修复：为 `@Scheduled` 设置时区，或在配置中统一时区。

```java
@Scheduled(cron = "0 0 8 * * *", zone = "Asia/Shanghai")
public void morningJob() {
    // ...
}
```

### 多任务阻塞：线程池限制

症状：某个任务正常执行，但其他任务迟迟不触发。

原因：默认只有一个调度线程，前面的任务阻塞了后面的任务。

修复：自定义线程池或避免单个任务过慢。

```java
@Configuration
public class SchedulingPoolConfig implements SchedulingConfigurer {
    @Override
    public void configureTasks(ScheduledTaskRegistrar taskRegistrar) {
        taskRegistrar.setScheduler(Executors.newScheduledThreadPool(5));
    }
}
```

## 排查 Checklist

快速定位定时任务问题：

1. 是否加了 `@EnableScheduling`？
2. 方法是否 `public void` 且无参数？
3. 是否被 Spring 管理，比如加了 `@Component` / `@Service`？
4. 是否在同类内部自调用？
5. 任务内部是否抛异常？
6. cron 的时间是否因时区问题不一致？
7. 是否有慢任务阻塞其他任务？

## 项目实战示例

下面给出一个基于本项目的最小定时任务示例：

- 配置类开启调度。
- 每 10 秒打印一次“用户统计快照”日志。

```java
@Configuration
@EnableScheduling
public class ScheduleConfig {
}
```

```java
@Component
public class UserStatsJob {

    private static final Logger log = LoggerFactory.getLogger(UserStatsJob.class);

    @Scheduled(cron = "*/10 * * * * *")
    public void printUserStats() {
        log.info("[scheduled] user stats snapshot at {}", LocalDateTime.now());
    }
}
```

启动项目后，控制台每 10 秒会输出一条日志，说明定时任务已生效。

## 本章检查

- 能用下单流程解释为什么需要事务。
- 能说明 `@Transactional` 的“全部成功 / 全部失败”含义。
- 知道事务只控制数据库操作。
- 知道受检异常需要 `rollbackFor = Exception.class`。
- 知道同类内部调用会导致事务代理不生效。
- 能写出 `@EnableScheduling` 和 `@Scheduled` 最小示例。
- 能区分 `cron`、`fixedRate`、`fixedDelay`。
- 能用 checklist 排查定时任务不触发问题。
