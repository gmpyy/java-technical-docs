---
title: "RabbitMQ 消息队列"
description: "队列、交换机、消费者堆积、消息可靠性与延迟消息"
outline: [2, 3]
---

# RabbitMQ 消息队列

RabbitMQ 的核心链路是：生产者把消息发给交换机，交换机根据绑定关系投递到队列，消费者从队列消费消息。

## 整体架构

```text
Producer
  -> Exchange
  -> Binding
  -> Queue
  -> Consumer
```

| 概念 | 作用 |
| --- | --- |
| Queue | 保存等待消费的消息 |
| Exchange | 接收消息并按规则路由 |
| Binding | 绑定交换机和队列 |
| routing key | 生产者发送消息时携带的路由键 |
| bindingKey | 队列绑定交换机时声明的匹配规则 |

## 创建队列并发送消息

```java
@Configuration
public class RabbitConfig {
    @Bean
    public Queue orderQueue() {
        return new Queue("order.queue", true);
    }
}
```

```java
rabbitTemplate.convertAndSend("order.queue", "order created");
```

## 接收消息

```java
@Component
public class OrderConsumer {
    @RabbitListener(queues = "order.queue")
    public void handle(String message) {
        System.out.println("receive: " + message);
    }
}
```

默认情况下，同一个队列中的一条消息只会被一个消费者处理。多个消费者共同消费同一队列时，如果处理速度差异很大，慢消费者可能出现消息堆积。

## Fanout 交换机

Fanout 会把消息广播给所有绑定队列，适合多个微服务都需要接收相同事件的场景。

```java
@Bean
public FanoutExchange userExchange() {
    return new FanoutExchange("user.fanout");
}

@Bean
public Binding userCreatedBinding(Queue userQueue, FanoutExchange userExchange) {
    return BindingBuilder.bind(userQueue).to(userExchange);
}
```

## Direct 交换机

Direct 根据 routing key 精确匹配 bindingKey。

```java
@Bean
public DirectExchange orderDirectExchange() {
    return new DirectExchange("order.direct");
}

@Bean
public Binding paidBinding(Queue paidQueue, DirectExchange orderDirectExchange) {
    return BindingBuilder.bind(paidQueue)
            .to(orderDirectExchange)
            .with("order.paid");
}
```

## Topic 交换机

Topic 支持通配符，更适合路由规则复杂的场景。

```java
@Bean
public TopicExchange topicExchange() {
    return new TopicExchange("event.topic");
}

@Bean
public Binding orderEventBinding(Queue eventQueue, TopicExchange topicExchange) {
    return BindingBuilder.bind(eventQueue)
            .to(topicExchange)
            .with("order.*");
}
```

## 消息转换器

对象消息需要序列化。项目中常使用 JSON 消息转换器。

```java
@Bean
public MessageConverter messageConverter() {
    return new Jackson2JsonMessageConverter();
}
```

## MQ 消息可靠性

可靠性要分三个阶段看：

| 阶段 | 关注点 |
| --- | --- |
| 生产者到 Broker | 生产者确认、失败重试 |
| Broker 保存消息 | 队列、交换机、消息持久化 |
| 消费者处理消息 | 手动 ack、重试次数、死信队列 |

## 生产者确认

生产者确认用于判断消息是否到达交换机和队列。

```yaml
spring:
  rabbitmq:
    publisher-confirm-type: correlated
    publisher-returns: true
```

## 消费者消息可靠性

为了防止业务异常无限重试，需要设置重试次数限制，并把失败消息投递到死信队列或人工补偿。

```yaml
spring:
  rabbitmq:
    listener:
      simple:
        acknowledge-mode: auto
        retry:
          enabled: true
          max-attempts: 3
```

## 延迟消息

延迟消息常见两种方案：

1. 死信交换机 + TTL。
2. RabbitMQ 延迟消息插件。

```text
订单创建
  -> 延迟消息
  -> 到期投递
  -> 检查订单是否支付
  -> 未支付则关闭订单
```

::: tip 选择建议
如果不确定交换机类型，Topic 通常更灵活；如果只是广播，Fanout 更简单。
:::

