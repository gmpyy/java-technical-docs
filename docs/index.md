---
title: "Java 技术文档"
description: "从 Java 基础语法到 Spring Boot、RabbitMQ 与 Redis 的系统化学习路线"
outline: [2, 3]
---

# Java 技术文档

这是一份基于 `JAVA.md` 重新整理的 Java 后端学习文档。它不再把 PDF 或 Markdown 原文直接转成一堆 HTML，而是把知识点重新拆成章节，让源码本身就是可维护的 Markdown。

## 阅读路线

| 阶段 | 推荐章节 | 目标 |
| --- | --- | --- |
| 语言基础 | Java 基础、方法与 IO、字符串与集合 | 看懂 Java 代码的基本结构 |
| 面向对象 | static、继承、抽象类、接口 | 理解类、对象、能力抽象和复用方式 |
| Web 后端 | Spring Boot 项目结构、请求参数、依赖注入 | 能搭建标准分层项目 |
| 认证与稳定性 | JWT、验证码、事务、定时任务 | 能处理登录、鉴权和失败回滚 |
| 中间件 | RabbitMQ、Redis | 能理解消息、缓存、锁和高并发优化 |

## 章节地图

- [基础语法与类型](/java/basic)：Java 跨平台、注释、字面量、基本数据类型、命名规范。
- [方法、IO 与 JavaBean](/java/syntax)：文件读写、Scanner、类型转换、方法、重载、构造方法、JavaBean。
- [字符串与集合](/java/string-collections)：字符串比较、StringBuilder、StringJoiner、ArrayList、数组/List/Set/Map、枚举。
- [面向对象进阶](/java/oop)：static、工具类、继承、重写、抽象类、接口。
- [生态与数据库基础](/java/ecosystem-database)：Maven、MySQL 数据类型、SQL、约束、索引。
- [项目结构与分层](/springboot/project)：Spring Boot 目录、resources、DTO、entity、VO、各层职责。
- [请求参数、DI 与 MyBatis](/springboot/request-di-mybatis)：请求参数接收、注解、依赖注入、MyBatis。
- [Filter、Interceptor 与 CORS](/springboot/web-chain)：请求链路、过滤器、拦截器、全局 MVC 配置、跨域。
- [JWT 与验证码认证](/springboot/auth)：登录、Token、Session 验证码、用户上下文。
- [事务与定时任务](/springboot/reliability)：`@Transactional`、`@Scheduled`、排坑 checklist。
- [RabbitMQ 消息队列](/middleware/rabbitmq)：队列、交换机、可靠性、延迟消息。
- [Redis 基础与登录链路](/redis/basics)：Redis 类型、短信验证码、登录拦截器。
- [缓存、锁与秒杀](/redis/cache-lock)：缓存穿透、缓存击穿、分布式锁、Redisson、异步秒杀。
- [Redis 高级结构](/redis/advanced)：List 队列、Stream、GEO、Bitmap、HyperLogLog。

## 文档约定

::: tip 重点
每章都保留关键代码块，并把散乱笔记改成“概念 → 写法 → 注意点 → 快速检查”的结构。
:::

```text
Markdown 源文件
  └─ VitePress 默认主题
      └─ 静态站点，可部署到 GitHub Pages / Cloudflare Pages
```

