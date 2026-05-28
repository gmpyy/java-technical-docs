---
title: "RabbitMQ 消息队列"
description: "RabbitMQ 整体架构、队列、交换机、消费者堆积、消息可靠性与延迟消息"
outline: [2, 4]
---

# RabbitMQ 消息队列

这一章对应 `JAVA.md` 中完整 RabbitMQ 部分。这里保留源笔记的所有 RabbitMQ 图片：整体架构、Java 使用、生产/消费、消费者堆积、Fanout、Direct、Topic、声明队列和交换机、消息转换器、可靠性和延迟消息。

## 整体架构

![RabbitMQ 整体架构](/images/source/image-22.png)

RabbitMQ 的核心链路：

```text
Producer
  -> Exchange
  -> Binding
  -> Queue
  -> Consumer
```

使用要点：

- `queues` 创建队列。
- `exchange` 通过 `binding` 来绑定队列。
- `exchange` 通过 `publish` 发送消息。
- admin 页面创建用户以及虚拟主机之后，可以实现数据隔离。

| 概念 | 作用 |
| --- | --- |
| Producer | 生产者，发送消息 |
| Exchange | 交换机，接收消息并按规则路由 |
| Binding | 绑定关系，把交换机和队列连接起来 |
| Queue | 队列，保存等待消费的消息 |
| Consumer | 消费者，从队列中取消息处理 |

## Java 中使用 MQ

### 引入依赖

首先引入依赖：

![RabbitMQ 引入依赖](/images/source/image-23.png)

### 配置基本信息

![RabbitMQ 配置基本信息](/images/source/image-24.png)

常见配置示例：

```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
    virtual-host: /
```

### 发送消息

![RabbitMQ 发送消息](/images/source/image-25.png)

常见发送代码：

```java
rabbitTemplate.convertAndSend("order.exchange", "order.created", message);
```

### 接收消息

![RabbitMQ 接收消息](/images/source/image-26.png)

常见监听代码：

```java
@RabbitListener(queues = "order.queue")
public void handleOrderMessage(String message) {
    System.out.println("receive: " + message);
}
```

## 绑定多个消费者的消费堆积问题

默认情况下，一条消息只能被一个消费者处理，不会出现两个消费者处理同一条消息的情况。

但是，如果一个队列绑定了两个消费者，一个处理得快，一个处理得慢，默认可能仍然平均分配消息，一人处理一半，导致处理慢的消费者出现消息堆积，要过很久才处理完。

解决办法：设置 `prefetch`，让处理快的消费者多处理一些消息，实现“能者多劳”。

![RabbitMQ prefetch 解决消费者堆积](/images/source/image-27.png)

配置示例：

```yaml
spring:
  rabbitmq:
    listener:
      simple:
        prefetch: 1
```

## Fanout 交换机

Fanout 交换机让不同微服务都接收相同消息。

![Fanout 交换机](/images/source/image-28.png)

发送消息给交换机：

![Fanout 发送消息给交换机](/images/source/image-29.png)

Fanout 的特点：

- 不关心 routing key。
- 发送给交换机的消息会投递给所有绑定的队列。
- 适合广播事件，例如“用户创建成功”后多个服务都需要感知。

## Direct 交换机

Direct 交换机发送消息时传不同的 `routingKey`，将消息发送到相同 `bindingKey` 的队列中。

当然，Direct 也可以实现 Fanout 交换机的效果：只需要所有队列都绑定同一个 `bindingKey`。

![Direct 交换机](/images/source/image-30.png)

示意：

```text
routingKey = order.paid
  -> bindingKey = order.paid 的队列收到消息
```

## Topic 交换机

Topic 交换机比较全能，如果不知道使用什么交换机，可以优先考虑 Topic。

![Topic 交换机](/images/source/image-31.png)

上图的意思：

- `queue1` 只关注 `china` 的消息。
- `queue2` 只关注 `japan` 的消息。
- `queue3` 只关注天气消息。
- `queue4` 只关注新闻消息。

Topic 常用通配符：

| 通配符 | 含义 |
| --- | --- |
| `*` | 匹配一个单词 |
| `#` | 匹配零个或多个单词 |

示例：

```text
china.weather
japan.news
china.news
```

## 声明队列和交换机基础写法

![声明队列和交换机基础写法](/images/source/image-32.png)

注解声明：

![注解声明队列和交换机](/images/source/image-33.png)

常见 Java Config 写法：

```java
@Bean
public Queue orderQueue() {
    return QueueBuilder.durable("order.queue").build();
}

@Bean
public TopicExchange orderExchange() {
    return new TopicExchange("order.topic");
}

@Bean
public Binding orderBinding(Queue orderQueue, TopicExchange orderExchange) {
    return BindingBuilder.bind(orderQueue)
            .to(orderExchange)
            .with("order.#");
}
```

## 消息转换器对对象消息进行序列化

![消息转换器](/images/source/image-34.png)

对象消息需要序列化。项目中常使用 JSON 消息转换器：

```java
@Bean
public MessageConverter messageConverter() {
    return new Jackson2JsonMessageConverter();
}
```

## MQ 消息可靠性

可靠性要分阶段看：

| 阶段 | 关注点 |
| --- | --- |
| 生产者到交换机 | 生产者确认 |
| 交换机到队列 | 路由失败处理 |
| 队列保存消息 | 持久化 |
| 消费者消费消息 | ACK、重试、死信 |

### 生产者重连

![生产者重连](/images/source/image-35.png)

由于重连是阻塞等待，比较影响性能，一般不作为主要方案。

### 生产者确认保障可靠性

![生产者确认 1](/images/source/image-36.png)

![生产者确认 2](/images/source/image-37.png)

生产者确认用于判断消息是否成功到达交换机，以及是否成功路由到队列。

常见配置：

```yaml
spring:
  rabbitmq:
    publisher-confirm-type: correlated
    publisher-returns: true
```

### MQ 可靠性

![MQ 可靠性](/images/source/image-38.png)

整体思路：

- 生产者确认消息是否到达。
- 交换机、队列、消息都尽量持久化。
- 消费者处理失败要有重试和兜底。

### 消费者消息可靠性

![消费者消息可靠性 1](/images/source/image-39.png)

![消费者消息可靠性 2](/images/source/image-40.png)

为了防止业务异常无限重试，需要设置重试次数限制：

![消费者重试限制 1](/images/source/image-41.png)

![消费者重试限制 2](/images/source/image-42.png)

![消费者重试限制 3](/images/source/image-43.png)

配置示例：

```yaml
spring:
  rabbitmq:
    listener:
      simple:
        retry:
          enabled: true
          max-attempts: 3
          initial-interval: 1000ms
          multiplier: 2
```

总结：

![MQ 消息可靠性总结](/images/source/image-44.png)

## 延迟消息

延迟消息常用于订单超时取消、延迟通知、定时补偿等场景。

### 死信交换机实现延迟消息

![死信交换机实现延迟消息](/images/source/image-45.png)

基本思路：

```text
业务消息
  -> 设置 TTL 的队列
  -> 到期后变成死信
  -> 投递到死信交换机
  -> 消费者处理延迟任务
```

### 插件实现延迟消息

![插件实现延迟消息 1](/images/source/image-46.png)

![插件实现延迟消息 2](/images/source/image-47.png)

插件方案通常更直接，但需要 RabbitMQ 安装延迟消息插件。

## 本章检查

- 能说清 Producer、Exchange、Binding、Queue、Consumer 的关系。
- 知道虚拟主机可以做数据隔离。
- 能说明为什么多个消费者消费同一队列时可能堆积。
- 能解释 `prefetch` 的作用。
- 能区分 Fanout、Direct、Topic。
- 能声明队列、交换机和绑定关系。
- 知道对象消息需要消息转换器序列化。
- 能按生产者、Broker、消费者三个阶段理解 MQ 可靠性。
- 能说出死信交换机和插件两种延迟消息方案。
