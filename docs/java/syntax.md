---
title: "方法、IO 与 JavaBean"
description: "流和文件读写、键盘录入、类型转换、方法、重载、构造方法与标准 Java 类"
outline: [2, 4]
---

# 方法、IO 与 JavaBean

这一章对应 `JAVA.md` 中从“流和文件读写”到“ptg 生成标准 Java 类”的内容。相比上一版摘要，这里保留源笔记中的完整示例和判断规则。

## 流和文件读写

Java IO 可以先按照“二进制 / 文本”和“普通流 / 缓冲流”理解。

| 类别 | 适用数据 | 常用类 |
| --- | --- | --- |
| 字节普通流 | 二进制 | `FileInputStream` / `FileOutputStream` |
| 字符普通流 | 文本 | `FileReader` / `FileWriter` |
| 字节缓冲流 | 二进制 | `BufferedInputStream` / `BufferedOutputStream` |
| 字符缓冲流 | 文本 | `BufferedReader` / `BufferedWriter` |

源笔记中的标准写法：输出流需要手动 `close()`。

```java
import java.io.*;

// 标准写法，输出流需要 close()
public class FileByteExample {
    public static void main(String[] args) throws IOException {
        FileInputStream fis = new FileInputStream("input.jpg");
        FileOutputStream fos = new FileOutputStream("output.jpg");

        int b;
        while ((b = fis.read()) != -1) {
            fos.write(b);
        }

        fos.close();
        fis.close();
    }
}
```

源笔记中的 `try-with-resources` 写法：不需要手动写 `close()`，离开 `try` 代码块时会自动关闭资源。

```java
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class BufferedStreamExample {
    public static void main(String[] args) throws IOException {
        try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream("input.txt"));
             BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream("output.txt"))) {

            byte[] buf = new byte[1024];
            int len;

            while ((len = bis.read(buf)) != -1) {
                bos.write(buf, 0, len);
            }
        }
    }
}
```

::: tip 使用建议
新代码优先使用 `try-with-resources`。它不是语法糖好看一点而已，真正的价值是避免异常场景下忘记关闭流。
:::

## 键盘录入

使用 `Scanner` 可以从控制台接收键盘输入。源笔记里的步骤是：导包、创建对象、接收数据。

```java
// 导包，其实就是先找到 Scanner 这个类在哪
import java.util.Scanner;

public class ScannerDemo1 {
    public static void main(String[] args) {
        // 2. 创建对象，其实就是声明一下，我准备开始用 Scanner 这个类了
        Scanner sc = new Scanner(System.in);

        // 3. 接收数据
        // 当程序运行之后，我们在键盘输入的数据就会被变量 i 接收
        System.out.println("请输入一个数字");
        int i = sc.nextInt();
        System.out.println(i);
    }
}
```

常用快捷编写代码：

```text
psvm -> public static void main(String[] args)
sout -> System.out.println()
```

示例：

```java
package com.itheima;

public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

## 隐式转换

隐式转换发生在数据类型不一致的时候。

取值范围可以先按这个顺序记：

```text
byte < short < int < long < float < double
```

转换规则：

- 范围小的类型会转换为计算式中范围最大的类型，再进行运算。
- `byte`、`short`、`char` 三种类型参与计算时，会自动转换为 `int`。

```java
byte a = 10;
byte b = 20;

// byte c = a + b; // 错误：a + b 会先提升为 int
int c = a + b;
System.out.println(c);
```

## 强制转换

强制转换用于把范围大的类型转为范围小的类型。语法是在数据或变量前面写目标类型。

源笔记示例：把 `double` 类型的 `a` 强制转换为 `int` 类型的 `b`。

```java
public class OperatorDemo2 {
    public static void main(String[] args) {
        double a = 12.3;
        int b = (int) a;

        System.out.println(b); // 12
    }
}
```

::: warning 注意
强制转换可能导致精度丢失。比如 `12.3` 转成 `int` 后会变成 `12`，小数部分会被直接舍弃。
:::

## 方法的通用格式

方法的格式：

```java
public static 返回值类型 方法名(参数) {
    方法体;
    return 数据;
}
```

各部分含义：

| 组成 | 说明 |
| --- | --- |
| `public static` | 修饰符，入门阶段可以先记住这个格式 |
| 返回值类型 | 方法操作完毕之后返回的数据的数据类型 |
| `void` | 如果方法操作完毕没有数据返回，返回值类型写 `void`，方法体中一般不写 `return 数据` |
| 方法名 | 调用方法时使用的标识 |
| 参数 | 由数据类型和变量名组成，多个参数之间用逗号隔开 |
| 方法体 | 完成功能的代码块 |
| `return` | 如果方法操作完毕有数据返回，用于把数据返回给调用者 |

示例：

```java
public class MethodDemo {
    public static int add(int left, int right) {
        int result = left + right;
        return result;
    }

    public static void main(String[] args) {
        int sum = add(10, 20);
        System.out.println(sum);
    }
}
```

## 方法重载

方法重载指同一个类中定义的多个方法之间的关系。满足下列条件的多个方法相互构成重载：

- 多个方法在同一个类中。
- 多个方法具有相同的方法名。
- 多个方法的参数不相同，可以是类型不同，也可以是数量不同。

注意：

- 重载只对应方法的定义，与方法的调用无关，调用方式参照标准格式。
- 重载只针对同一个类中的方法名称与参数进行识别，与返回值无关。
- 换句话说，不能通过返回值来判定两个方法是否相互构成重载。

### 正确范例

参数类型不同，可以构成重载：

```java
public class MethodDemo {
    public static void fn(int a) {
        // 方法体
    }

    public static int fn(double a) {
        // 方法体
        return 0;
    }
}
```

参数数量不同，也可以构成重载：

```java
public class MethodDemo {
    public static float fn(int a) {
        // 方法体
        return 0.0F;
    }

    public static int fn(int a, int b) {
        // 方法体
        return 0;
    }
}
```

### 错误范例

返回值不同但参数相同，不能构成重载：

```java
public class MethodDemo {
    public static void fn(int a) {
        // 方法体
    }

    public static int fn(int a) {
        // 错误原因：重载与返回值无关
        return 0;
    }
}
```

两个方法不在同一个类中，也不能说它们互相重载：

```java
public class MethodDemo01 {
    public static void fn(int a) {
        // 方法体
    }
}

public class MethodDemo02 {
    public static int fn(double a) {
        // 错误原因：这是两个类的两个 fn 方法
        return 0;
    }
}
```

## 构造方法

构造方法是一种特殊的方法。

作用：

```java
Student stu = new Student();
```

创建对象时，构造方法会自动执行，主要用于完成对象数据的初始化。

格式：

```java
public class 类名 {
    修饰符 类名(参数) {
    }
}
```

示例代码：

```java
class Student {
    private String name;
    private int age;

    // 构造方法
    public Student() {
        System.out.println("无参构造方法");
    }

    public void show() {
        System.out.println(name + "," + age);
    }
}

/*
    测试类
 */
public class StudentDemo {
    public static void main(String[] args) {
        // 创建对象
        Student s = new Student();
        s.show();
    }
}
```

## PTG 生成标准 Java 类

标准 Java 类通常包含这些部分：

1. 私有化全部成员变量。
2. 空参构造。
3. 带全部参数的构造。
4. 针对于每一个私有化的成员变量都提供对应的 `get` 和 `set` 方法。
5. 如果当前事物还有其他行为，也要写出来，比如学生的吃饭、睡觉等行为。

源笔记中的完整示例：

```java
public class User {
    // 1. 私有化全部的成员变量
    // 2. 空参构造
    // 3. 带全部参数的构造
    // 4. 针对于每一个私有化的成员变量都要提供其对应的 get 和 set 方法
    // 5. 如果当前事物还有其他行为，那么也要写出来，比如学生的吃饭、睡觉等行为

    private String username; // 用户名
    private String password; // 密码
    private String email;    // 邮箱
    private char gender;     // 性别
    private int age;         // 年龄

    // 空参构造方法
    public User() {
    }

    // 带全部参数的构造
    public User(String username, String password, String email, char gender, int age) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.gender = gender;
        this.age = age;
    }

    // get 和 set
    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public char getGender() {
        return gender;
    }

    public void setGender(char gender) {
        this.gender = gender;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public void eat() {
        System.out.println(username + "在吃饭");
    }
}
```

安装 PTG 之后，右键鼠标就能选择使用 PTG 自动生成标准类。这个工具可以提高效率，但你仍然要知道标准类应该由哪些部分组成。

## 本章检查

- 能区分字节流、字符流、缓冲流。
- 能用 `Scanner` 接收键盘输入。
- 能说清隐式转换和强制转换的区别。
- 能写出方法的通用格式。
- 能判断两个方法是否构成重载。
- 能写出构造方法和标准 Java 类的基本结构。
