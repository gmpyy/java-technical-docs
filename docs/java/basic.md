---
title: "基础语法与类型"
description: "Java 跨平台原理、注释、字面量、基本数据类型与命名规范"
outline: [2, 3]
---

# 基础语法与类型

这一章整理 Java 入门阶段最容易混在一起的概念：跨平台、注释、字面量、基本数据类型、类型后缀和命名规范。

## Java 跨平台

Java 语言不是直接运行在操作系统上，而是运行在 JVM 上。源代码经过编译后生成字节码，不同操作系统只要安装对应的 JVM，就能运行同一份字节码。

```text
Java 源码 (.java)
  -> 编译器 javac
  -> 字节码 (.class)
  -> JVM
  -> Windows / Linux / macOS
```

| 名称 | 作用 |
| --- | --- |
| JDK | Java Development Kit，开发工具包，包含编译器和运行环境 |
| JRE | Java Runtime Environment，只提供运行 Java 程序需要的环境 |
| JVM | Java Virtual Machine，负责加载、验证和执行字节码 |

## 注释

Java 常见注释有三类：

```java
// 单行注释：说明一行代码

/*
 多行注释：说明一段代码或临时屏蔽代码
*/

/**
 * 文档注释：用于类、方法、字段，可生成 API 文档
 */
```

::: warning 注意
注释解释“为什么这样写”和“这里有什么约束”，不要把每行代码翻译一遍。
:::

## 字面量

字面量是代码里直接写出来的数据值。字符串和字符要分清：

| 类型 | 示例 | 说明 |
| --- | --- | --- |
| 字符串 | `"hello"` | 双引号，可以包含多个字符 |
| 字符 | `'a'` | 单引号，只表示单个字符 |
| 整数 | `10` | 默认是 `int` |
| 小数 | `3.14` | 默认是 `double` |
| 布尔 | `true` / `false` | 用于条件判断 |

制表符 `\t` 可以补齐到制表位，适合简单命令行输出，但正式文档和页面布局不要依赖它。

## 基本数据类型

Java 有 8 种基本数据类型：

| 类别 | 类型 | 常见用途 |
| --- | --- | --- |
| 整数 | `byte`、`short`、`int`、`long` | 年龄、数量、ID、计数 |
| 浮点 | `float`、`double` | 小数计算，金额不建议使用浮点 |
| 字符 | `char` | 单个字符 |
| 布尔 | `boolean` | 条件开关 |

```java
public class VariableDemo {
    public static void main(String[] args) {
        byte age = 18;
        short year = 2026;
        int count = 1000;
        long orderId = 123456789123L;
        float score = 98.5F;
        double price = 19.9;
        char level = 'A';
        boolean enabled = true;

        System.out.println(age);
        System.out.println(orderId);
        System.out.println(enabled);
    }
}
```

### 后缀规则

- 定义 `long` 字面量时，建议在数值后加 `L`。
- 定义 `float` 字面量时，必须在数值后加 `F`。
- `double` 是默认浮点类型，通常不需要额外后缀。

## 命名规范

### 小驼峰命名法

适用于变量名和方法名：

```java
String name = "tom";
int maxAge = 30;

public void findUserById() {
    // ...
}
```

### 大驼峰命名法

适用于类名：

```java
public class HelloWorld {
}

public class UserService {
}
```

## 快速检查

- 能说清 Java 跨平台依赖 JVM，而不是源码直接跨平台。
- 能区分字符 `'a'` 和字符串 `"a"`。
- 能记住 `long` 用 `L`，`float` 用 `F`。
- 类名使用大驼峰，变量和方法使用小驼峰。

