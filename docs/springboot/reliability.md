---
title: "事务与定时任务"
description: "@Transactional、事务回滚、@Scheduled 定时任务与排坑 checklist"
outline: [2, 3]
---

# 事务与定时任务

这一章整理两个后端稳定性基础：事务保证数据库操作一致性，定时任务保证周期性逻辑按预期触发。

## 如果没有事务

典型下单流程：

1. 扣库存。
2. 扣余额。
3. 生成订单。

如果前两步成功，第三步失败，而没有事务保护，就会产生数据不一致。

```text
扣库存成功 -> 扣余额成功 -> 写订单失败
结果：用户钱扣了，订单却不存在
```

## 使用 @Transactional

`@Transactional` 把多个数据库操作绑定成一个整体：要么全部成功，要么出现异常后整体回滚。

```java
@Service
public class OrderService {
    @Transactional
    public void createOrder(Long userId, Long productId, BigDecimal amount) {
        inventoryRepository.decrease(productId, 1);
        accountRepository.decreaseBalance(userId, amount);
        orderRepository.insertOrder(userId, productId, amount);
    }
}
```

## 事务常见误区

| 误区 | 说明 |
| --- | --- |
| 事务只对数据库操作生效 | 已发送的 MQ、HTTP 请求不会自动撤销 |
| 默认回滚运行时异常 | 受检异常需要配置 `rollbackFor` |
| 自调用事务失效 | 同类内部调用不会经过 Spring 代理 |

```java
@Transactional(rollbackFor = Exception.class)
public void importData() throws Exception {
    // 需要受检异常也回滚时，显式配置 rollbackFor
}
```

## 定时任务最小可用概念

使用 `@Scheduled` 前必须开启定时能力。

```java
@EnableScheduling
@SpringBootApplication
public class StudyApplication {
    public static void main(String[] args) {
        SpringApplication.run(StudyApplication.class, args);
    }
}
```

## 三种常见写法

```java
@Component
public class ReportTask {
    @Scheduled(fixedRate = 5000)
    public void fixedRateTask() {
        System.out.println("每 5 秒执行一次");
    }

    @Scheduled(fixedDelay = 5000)
    public void fixedDelayTask() {
        System.out.println("上次结束 5 秒后执行");
    }

    @Scheduled(cron = "*/5 * * * * *")
    public void cronTask() {
        System.out.println("cron 每 5 秒执行一次");
    }
}
```

## 为什么定时任务不触发

排查顺序：

- 是否添加 `@EnableScheduling`。
- 方法是否是 `public void` 且无参数。
- 类是否被 Spring 管理，例如有 `@Component` 或 `@Service`。
- 是否在同类内部自调用。
- 任务内部是否抛出异常。
- cron 时区是否和预期一致。
- 是否被慢任务阻塞。

## 项目实战建议

```java
@Scheduled(cron = "0 */10 * * * *", zone = "Asia/Shanghai")
public void refreshCache() {
    try {
        cacheService.refreshHotData();
    } catch (Exception ex) {
        log.error("refresh hot data failed", ex);
    }
}
```

::: warning 注意
定时任务内部要捕获并记录异常，避免一次异常让后续调度表现异常。
:::

