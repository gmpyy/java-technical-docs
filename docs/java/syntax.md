---
title: "方法、IO 与 JavaBean"
description: "整理流和文件读写、Scanner、类型转换、方法、重载、构造方法与 JavaBean"
outline: [2, 3]
---

# 方法、IO 与 JavaBean

这一章把原笔记中分散的 IO、键盘录入、类型转换、方法、构造方法和标准 Java 类整理成一条语言基础线。

## 流和文件读写

Java IO 可以先按“二进制 / 文本”和“普通流 / 缓冲流”理解：

| 类型 | 二进制 | 文本 |
| --- | --- | --- |
| 普通流 | `FileInputStream` / `FileOutputStream` | `FileReader` / `FileWriter` |
| 缓冲流 | `BufferedInputStream` / `BufferedOutputStream` | `BufferedReader` / `BufferedWriter` |

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class FileByteExample {
    public static void main(String[] args) throws IOException {
        try (FileInputStream input = new FileInputStream("input.jpg");
             FileOutputStream output = new FileOutputStream("output.jpg")) {
            int value;
            while ((value = input.read()) != -1) {
                output.write(value);
            }
        }
    }
}
```

::: tip 建议
优先使用 `try-with-resources`，让流自动关闭，避免遗漏 `close()`。
:::

## 键盘录入

`Scanner` 用于从控制台接收输入：

```java
import java.util.Scanner;

public class ScannerDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("请输入一个数字：");
        int value = scanner.nextInt();

        System.out.println("你输入的是：" + value);
    }
}
```

常用快捷写法：

```text
psvm -> public static void main(String[] args)
sout -> System.out.println()
```

## 隐式转换

当数据类型不一致时，范围小的类型会自动转换为表达式中范围更大的类型：

```text
byte < short < int < long < float < double
```

`byte`、`short`、`char` 三种类型参与运算时会先提升为 `int`。

```java
byte a = 10;
byte b = 20;

// byte result = a + b; // 编译错误，因为 a + b 的结果是 int
int result = a + b;
System.out.println(result);
```

## 强制转换

强制转换用于把范围大的类型转成范围小的类型，但可能丢失精度。

```java
public class CastDemo {
    public static void main(String[] args) {
        double price = 12.8;
        int value = (int) price;

        System.out.println(value); // 12
    }
}
```

## 方法的通用格式

方法是把一段逻辑命名，并通过参数和返回值形成可复用接口。

```java
修饰符 返回值类型 方法名(参数列表) {
    方法体;
    return 返回值;
}
```

示例：

```java
public class MethodDemo {
    public static int add(int left, int right) {
        return left + right;
    }

    public static void main(String[] args) {
        int result = add(10, 20);
        System.out.println(result);
    }
}
```

## 方法重载

方法重载指同一个类中方法名相同，但参数列表不同。参数列表不同可以是参数个数不同、类型不同或顺序不同。

```java
public class OverloadDemo {
    public static int sum(int a, int b) {
        return a + b;
    }

    public static double sum(double a, double b) {
        return a + b;
    }

    public static int sum(int a, int b, int c) {
        return a + b + c;
    }
}
```

## 构造方法

构造方法用于创建对象时初始化状态。它没有返回值，方法名必须和类名一致。

```java
public class User {
    private String name;
    private int age;

    public User() {
    }

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

## JavaBean

标准 JavaBean 通常包含私有属性、无参构造、带参构造、getter 和 setter。

```java
public class Student {
    private String name;
    private int age;

    public Student() {
    }

    public Student(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

