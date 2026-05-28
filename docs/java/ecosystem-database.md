---
title: "生态与数据库基础"
description: "Maven、MySQL 数据类型、SQL、约束与索引"
outline: [2, 3]
---

# 生态与数据库基础

Java 后端项目通常离不开 Maven 和数据库。本章整理 Maven 的定位，以及 MySQL 中常见的数据类型、SQL、约束和索引。

## Maven

Maven 主要解决依赖管理、项目结构约定和构建流程问题。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

Maven 常见目录结构：

```text
project
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   └── resources
    └── test
        └── java
```

## MySQL 常用数据类型

| 类型 | 适合场景 | 说明 |
| --- | --- | --- |
| `BIGINT` | 主键、业务 ID | 比 `INT` 范围更大 |
| `VARCHAR` | 名称、手机号、状态值 | 可变长度字符串 |
| `TEXT` | 长描述、备注 | 不适合频繁索引 |
| `DECIMAL` | 金额 | 避免浮点误差 |
| `DATETIME` | 创建时间、更新时间 | 常用于业务时间 |

## 常用 SQL

```sql
CREATE TABLE user_account (
    id BIGINT PRIMARY KEY,
    phone VARCHAR(20) NOT NULL UNIQUE,
    nickname VARCHAR(64) DEFAULT '新用户',
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL
);

INSERT INTO user_account (id, phone, nickname, created_at)
VALUES (1, '13800000000', 'tom', NOW());

SELECT id, phone, nickname
FROM user_account
WHERE phone = '13800000000';
```

## SQL 的属性与约束

| 约束 | 作用 |
| --- | --- |
| `PRIMARY KEY` | 主键，唯一标识一行数据 |
| `UNIQUE` | 保证字段不重复 |
| `NOT NULL` | 字段不能为空 |
| `DEFAULT` | 字段默认值 |
| `AUTO_INCREMENT` | 自增值 |

::: tip 建议
约束不是替代业务校验，而是数据库层面的最后一道保护。
:::

## SQL 索引

索引用于加速查询，但会增加写入成本和存储成本。

```sql
CREATE INDEX idx_user_phone ON user_account(phone);
```

适合建索引的字段：

- 经常出现在 `WHERE` 条件中的字段。
- 经常用于关联的字段。
- 选择性较高的字段。

不适合盲目建索引的场景：

- 数据量很小。
- 字段取值重复率很高。
- 写入非常频繁且查询不依赖该字段。

