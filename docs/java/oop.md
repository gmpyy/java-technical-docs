---
title: "面向对象进阶"
description: "static、工具类、继承、重写、重载、构造方法、抽象类与接口"
outline: [2, 3]
---

# 面向对象进阶

面向对象的重点不是“语法更多”，而是把职责放在合适的类里，并通过继承、抽象类和接口表达复用与能力边界。

## static 静态变量

`static` 修饰的成员属于类，不属于某个对象。所有对象共享同一份静态变量。

```java
public class UserCounter {
    public static int total = 0;

    public UserCounter() {
        total++;
    }
}
```

::: warning 注意
静态变量是共享状态，项目中要谨慎使用，避免隐藏的数据污染。
:::

## 工具类

工具类通常只包含静态方法，不保存对象状态。为了避免被实例化，构造方法可以私有化。

```java
public final class StringUtils {
    private StringUtils() {
    }

    public static boolean hasText(String value) {
        return value != null && !value.trim().isEmpty();
    }
}
```

## 静态方法注意事项

静态方法只能直接访问静态成员，不能直接访问非静态成员，因为它不依赖对象实例。

```java
public class StaticDemo {
    private String name;
    private static int count;

    public static void printCount() {
        System.out.println(count);
        // System.out.println(name); // 编译错误
    }
}
```

## 继承

继承表达“is-a”关系，子类可以复用父类的属性和方法。

```java
public class Animal {
    public void eat() {
        System.out.println("eat");
    }
}

public class Dog extends Animal {
    public void bark() {
        System.out.println("bark");
    }
}
```

继承规则：

- Java 只支持单继承，一个类只能直接继承一个父类。
- Java 支持多层继承。
- 子类可以访问父类中可见的成员。

## 方法重写

方法重写指子类重新实现父类已有方法。重写时方法名、参数列表和返回值类型要兼容。

```java
public class Cat extends Animal {
    @Override
    public void eat() {
        System.out.println("cat eats fish");
    }
}
```

## 方法重载

方法重载发生在同一个类中，方法名相同但参数列表不同。重载是编译期根据参数决定调用哪个方法。

```java
public class Printer {
    public void print(String value) {
        System.out.println(value);
    }

    public void print(int value) {
        System.out.println(value);
    }
}
```

## 继承中的构造方法

创建子类对象时，会先调用父类构造方法，再调用子类构造方法。可以使用 `super()` 指定父类构造。

```java
public class Parent {
    public Parent(String name) {
        System.out.println(name);
    }
}

public class Child extends Parent {
    public Child() {
        super("parent");
    }
}
```

## 抽象类

抽象类可以包含抽象方法，也可以包含普通方法。它适合表达“共同父类 + 部分实现”。

```java
public abstract class Payment {
    public abstract void pay();

    public void printLog() {
        System.out.println("payment log");
    }
}
```

## 接口

接口表达能力规范。一个类可以实现多个接口，因此接口更适合描述横向能力。

```java
public interface MessageSender {
    void send(String message);
}

public class EmailSender implements MessageSender {
    @Override
    public void send(String message) {
        System.out.println("send email: " + message);
    }
}
```

| 对比项 | 抽象类 | 接口 |
| --- | --- | --- |
| 关注点 | 共同父类和复用实现 | 能力约束和扩展点 |
| 继承数量 | 单继承 | 可实现多个 |
| 使用场景 | 模板方法、公共字段、公共流程 | 插件能力、策略、适配器 |

