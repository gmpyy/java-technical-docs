---
title: "基础语法与类型"
description: "Java 跨平台原理、注释、字面量、基本数据类型与命名规范"
outline: [2, 4]
---

# 基础语法与类型

这一章对应 `JAVA.md` 开头的 Java 入门内容，保留原始知识点：重要技术点、跨平台运行原理、注释、字面量、基本数据类型和命名规范。

## JAVA

这份文档围绕后端学习中常见的 Java 技术栈展开。

## 重要技术点

原笔记中列出的重点方向：

- MySQL
- Redis
- JVM
- 消息队列

这些内容会在后续章节中继续展开：MySQL 放在生态与数据库章节，消息队列放在 RabbitMQ 章节，Redis 单独拆成 Redis 基础、缓存锁和高级结构三章。

## Java 跨平台运行的原理

Java 语言并不是直接运行在操作系统上，而是运行在虚拟机上。所以不同的操作系统只要安装该系统对应的虚拟机，就可以运行 Java 程序。

![Java 跨平台运行原理](/java-technical-docs/images/source/image-01.png)

可以把它理解成下面这条链路：

```text
Java 源代码 .java
  -> javac 编译
  -> 字节码 .class
  -> JVM 虚拟机
  -> Windows / Linux / macOS
```

关键点不是“源代码天然跨平台”，而是“字节码运行在不同平台对应的 JVM 上”。

| 名称 | 说明 |
| --- | --- |
| JDK | Java Development Kit，开发工具包，写代码和编译代码时需要 |
| JRE | Java Runtime Environment，Java 运行环境 |
| JVM | Java Virtual Machine，Java 虚拟机，负责执行字节码 |

## Java 的注释

![Java 注释类型](/java-technical-docs/images/source/image-02.png)

Java 的注释有三种：

- 单行注释
- 多行注释
- 文档注释

```java
// 单行注释：通常用于解释一行代码或一个小逻辑

/*
 多行注释：
 可以解释一段较长逻辑，
 也可以临时屏蔽多行代码。
*/

/**
 * 文档注释：
 * 常用于类、方法、字段上，
 * 可以配合工具生成 API 文档。
 */
```

写注释时更重要的是解释“为什么这么写”和“这里有什么限制”，不要只是把代码逐行翻译成中文。

## Java 的字面量

字面量就是代码中直接写出来的数据值。

值得注意的是，字符串和字符类型是分开的：

- 字符类型使用单引号：`'a'`
- 字符串类型使用双引号：`"abc"`

![Java 字面量](/java-technical-docs/images/source/image-03.png)

常见字面量示例：

| 字面量类型 | 示例 | 说明 |
| --- | --- | --- |
| 整数 | `10`、`100` | 默认是 `int` |
| 小数 | `3.14`、`10.5` | 默认是 `double` |
| 字符 | `'a'`、`'中'` | 单引号，只能表示单个字符 |
| 字符串 | `"hello"`、`"Java"` | 双引号，可以表示多个字符 |
| 布尔 | `true`、`false` | 常用于条件判断 |
| 空值 | `null` | 表示引用类型没有指向对象 |

制表符 `\t` 的作用是补齐到制表位，可以利用制表符实现简单的对齐效果：

```java
System.out.println("name\tage");
System.out.println("Tom\t18");
System.out.println("Jerry\t20");
```

## 基本数据类型

Java 有 8 种基本数据类型：`byte`、`short`、`int`、`long`、`float`、`double`、`char`、`boolean`。

```java
public class VariableDemo3 {
    public static void main(String[] args) {
        // 1. 定义 byte 类型的变量
        // 数据类型 变量名 = 数据值;
        byte a = 10;
        System.out.println(a);

        // 2. 定义 short 类型的变量
        short b = 20;
        System.out.println(b);

        // 3. 定义 int 类型的变量
        int c = 30;
        System.out.println(c);

        // 4. 定义 long 类型的变量
        long d = 123456789123456789L;
        System.out.println(d);

        // 5. 定义 float 类型的变量
        float e = 10.1F;
        System.out.println(e);

        // 6. 定义 double 类型的变量
        double f = 20.3;
        System.out.println(f);

        // 7. 定义 char 类型的变量
        char g = 'a';
        System.out.println(g);

        // 8. 定义 boolean 类型的变量
        boolean h = true;
        System.out.println(h);
    }
}
```

| 类型 | 占用空间 | 说明 |
| --- | --- | --- |
| `byte` | 1 字节 | 整数类型，范围较小 |
| `short` | 2 字节 | 整数类型 |
| `int` | 4 字节 | 最常用的整数类型 |
| `long` | 8 字节 | 大整数类型 |
| `float` | 4 字节 | 单精度浮点数 |
| `double` | 8 字节 | 双精度浮点数，Java 小数默认类型 |
| `char` | 2 字节 | 单个字符 |
| `boolean` | 未明确规定 | 只有 `true` 和 `false` |

### 注意点

- 如果要定义一个 `long` 类型的变量，那么在数据值的后面需要加上 `L` 后缀。大小写都可以，但建议使用大写 `L`。
- 如果要定义一个 `float` 类型的变量，那么在数据值的后面需要加上 `F` 后缀。大小写都可以，但建议使用大写 `F`。
- 整数默认是 `int`，小数默认是 `double`。

## 命名规范

命名规范影响代码可读性，也会影响团队协作。Java 中最常见的是小驼峰命名法和大驼峰命名法。

### 小驼峰命名法

适用于变量名和方法名。

- 如果是一个单词，那么全部小写，比如：`name`
- 如果是多个单词，那么从第二个单词开始，首字母大写，比如：`firstName`、`maxAge`

```java
String name = "Tom";
int maxAge = 18;

public void findUserById() {
    // ...
}
```

### 大驼峰命名法

适用于类名。

- 如果是一个单词，那么首字母大写，比如：`Demo`、`Test`
- 如果是多个单词，那么每一个单词首字母都需要大写，比如：`HelloWorld`

```java
public class Demo {
}

public class HelloWorld {
}
```

## 本章检查

- 能说清 Java 跨平台依赖 JVM，而不是源代码直接运行在所有操作系统上。
- 能区分单行注释、多行注释和文档注释。
- 能区分字符 `'a'` 和字符串 `"a"`。
- 能写出 8 种基本数据类型。
- 知道 `long` 后缀用 `L`，`float` 后缀用 `F`。
- 类名使用大驼峰，变量名和方法名使用小驼峰。
