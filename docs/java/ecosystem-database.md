---
title: "生态与数据库基础"
description: "Maven、MySQL 常用数据类型、SQL 语句、约束与索引"
outline: [2, 4]
---

# 生态与数据库基础

这一章对应 `JAVA.md` 中“java 相关生态”和“数据库”部分。源笔记以图片和简短清单为主，这里保留图片并补上必要的文字说明，方便在文档站里阅读。

## Java 相关生态

Java 后端学习不只包含 Java 语法，还会进入 Maven、数据库、Spring Boot、Redis、RabbitMQ 等生态工具。本章先放 Maven 与数据库基础，后面的章节会继续展开 Spring Boot、消息队列和 Redis。

## Maven

![Maven 说明 1](/java-technical-docs/images/source/image-06.png)

![Maven 说明 2](/java-technical-docs/images/source/image-07.png)

Maven 常用于解决三个问题：

- 项目结构约定：统一 `src/main/java`、`src/main/resources`、`src/test/java` 等目录。
- 依赖管理：通过 `pom.xml` 引入第三方依赖。
- 构建流程：执行编译、测试、打包等动作。

典型 `pom.xml` 依赖写法：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

典型 Maven 项目结构：

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

## 数据库

后端服务通常需要把数据持久化到数据库中。学习 Spring Boot 之前，至少要熟悉常见数据类型、SQL 语句、约束和索引。

### 常用数据类型

![MySQL 常用数据类型](/java-technical-docs/images/source/image-08.png)

常见 MySQL 类型：

| 类型 | 适合场景 | 说明 |
| --- | --- | --- |
| `INT` | 普通整数 | 比如数量、年龄等 |
| `BIGINT` | 大整数、主键 ID | 业务 ID 常用 |
| `VARCHAR` | 短文本 | 用户名、手机号、状态编码 |
| `TEXT` | 长文本 | 文章内容、备注 |
| `DECIMAL` | 精确小数 | 金额场景优先使用 |
| `DATETIME` | 日期时间 | 创建时间、更新时间 |

### 常用 SQL 语句

![常用 SQL 语句](/java-technical-docs/images/source/image-09.png)

常见 SQL 可以按增删改查记：

```sql
-- 建表
CREATE TABLE user_account (
    id BIGINT PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    phone VARCHAR(20) UNIQUE,
    created_at DATETIME
);

-- 新增
INSERT INTO user_account (id, username, phone, created_at)
VALUES (1, 'tom', '13800000000', NOW());

-- 查询
SELECT id, username, phone
FROM user_account
WHERE id = 1;

-- 修改
UPDATE user_account
SET username = 'jerry'
WHERE id = 1;

-- 删除
DELETE FROM user_account
WHERE id = 1;
```

### SQL 的属性与约束

源笔记中的约束清单：

| 约束 / 属性 | 说明 |
| --- | --- |
| `UNIQUE` | 唯一 |
| `NOT NULL` | 非空 |
| `CHECK` | 条件判断，通过则添加成功 |
| `PRIMARY KEY` | 主键约束，用于快速查询 |
| `FOREIGN KEY` | 外键约束，用于关联其他表 |
| `DEFAULT` | 默认值 |
| `AUTO_INCREMENT` | 自增，一个表只有一个，要求字段唯一且非空 |

示例：

```sql
CREATE TABLE orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(64) NOT NULL UNIQUE,
    user_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'UNFINISH',
    created_at DATETIME NOT NULL,
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_account(id)
);
```

::: warning 注意
数据库约束是最后一道保护。业务层也应该做参数校验，不能完全依赖数据库报错。
:::

### SQL 索引

![SQL 索引](/java-technical-docs/images/source/image-10.png)

索引用于提高查询速度。可以把索引理解为数据库为某些字段额外维护的一份“目录”。

```sql
CREATE INDEX idx_user_phone ON user_account(phone);
```

适合加索引的字段：

- 经常出现在 `WHERE` 条件中的字段。
- 经常作为关联条件的字段。
- 经常用于排序或分组的字段。
- 区分度比较高的字段。

不适合乱加索引的情况：

- 表数据量很小。
- 字段值重复率很高。
- 写入非常频繁，但查询并不依赖该字段。

索引会提升查询，但会增加写入和维护成本。实际项目里不要“看到字段就建索引”，要结合查询语句和数据量判断。

## 本章检查

- 知道 Maven 负责依赖管理、项目结构约定和构建流程。
- 能看懂基础 `pom.xml` 依赖。
- 能区分常见 MySQL 字段类型。
- 能写出基础增删改查 SQL。
- 能说出 `UNIQUE`、`NOT NULL`、`PRIMARY KEY`、`FOREIGN KEY`、`DEFAULT`、`AUTO_INCREMENT` 的作用。
- 能说明索引为什么能加快查询，以及为什么不能随便乱建索引。
