---
title: "面向对象进阶"
description: "static、工具类、继承、重写、重载、构造方法、抽象类与接口"
outline: [2, 4]
---

# 面向对象进阶

这一章对应 `JAVA.md` 中“面向对象进阶”部分，完整整理静态、工具类、继承、方法重写/重载、继承中的构造方法、抽象类和接口。

## 静态

### `static` 静态变量

`static` 表示静态变量，所有对象共享同一个静态变量。比如多个学生在同一个学校上学，学校名称就可以作为静态变量。

```java
public class Student {
    // 实例变量
    private String name;

    // static 就是静态变量，所有对象共享同一个静态变量
    public static String schoolName;

    public void run() {
        System.out.println("学生可以跑步");
    }
}
```

使用示例：

```java
public class StudentDemo {
    public static void main(String[] args) {
        Student.schoolName = "传智教育";

        Student stu = new Student();
        // stu.name = "徐干"; // name 是 private，真实代码中应通过 set 方法设置

        Student stu2 = new Student();
        // stu2.name = "李干";

        // 所有学生对象会共用同一个 schoolName
        System.out.println(Student.schoolName);
    }
}
```

::: warning 注意
静态变量属于类，不属于某一个对象。它方便共享数据，但也容易带来全局状态污染，业务代码中不要滥用。
:::

### 工具类

工具类通常不保存对象状态，主要提供静态方法。为了避免被创建对象，构造方法一般写成 `private`。

源笔记示例：通过工具类获取学生集合中的最大年龄。

学生类：

```java
public class Student {
    private String name;
    private int age;

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

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}
```

工具类：

```java
import java.util.ArrayList;

public class StudentUtils {
    // 构造方法必须是 private，避免外部创建工具类对象
    private StudentUtils() {
    }

    // 返回值是 int 类型，方法设置为静态方法
    public static int getMaxAgeStudent(ArrayList<Student> list) {
        int maxAge = list.get(0).getAge();

        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).getAge() > maxAge) {
                maxAge = list.get(i).getAge();
            }
        }

        return maxAge;
    }
}
```

调用工具类：

```java
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList<Student> list = new ArrayList<>();
        list.add(new Student("张三", 18));
        list.add(new Student("李四", 20));
        list.add(new Student("王五", 22));

        int maxAge = StudentUtils.getMaxAgeStudent(list);
        System.out.println(maxAge);
    }
}
```

### 静态方法注意事项

1. 静态方法中只能直接访问静态成员。
2. 非静态方法可以访问所有成员。
3. 静态方法中没有 `this` 关键字。

```java
public class StaticDemo {
    private String name;
    private static int count;

    public static void staticMethod() {
        System.out.println(count);
        // System.out.println(name); // 错误：静态方法不能直接访问非静态成员
        // System.out.println(this); // 错误：静态方法中没有 this
    }

    public void instanceMethod() {
        System.out.println(name);
        System.out.println(count);
        System.out.println(this);
    }
}
```

## 继承

### 继承的简单格式

```java
class 父类 {
    // ...
}

class 子类 extends 父类 {
    // ...
}
```

继承表达的是“子类是父类的一种”。子类可以复用父类中允许访问的成员。

### 继承的规则

1. 一个类最多只有一个父类。
2. 子类只能访问父类的非私有成员。
3. 子类打印自己的属性可以用 `this`，打印父类的属性可以用 `super`。

```java
class Fu {
    String name = "Fu";
    String hobby = "喝茶";
}

class Zi extends Fu {
    String name = "Zi";
    String game = "吃鸡";

    public void show() {
        String name = "cur";

        System.out.println(name);       // cur
        System.out.println(this.name);  // Zi
        System.out.println(super.name); // Fu
    }
}
```

还有一个就近原则：相当于前端对象中的原型链，在当前类上找不到的属性，会沿着继承链向上查找。

### 方法的重写

子类可以对父类已有方法进行重写。方法名称和参数列表保持一致，方法体重新实现。

```java
public class Animal {
    public void cry() {
        System.out.println("动物都可以叫~~~");
    }
}
```

```java
public class Cat extends Animal {
    // 声明不变，重新实现
    // 方法名称与父类全部一样，只是方法体中的功能重写了
    // 重写要使用 @Override 注解
    @Override
    public void cry() {
        System.out.println("我们一起学猫叫，喵喵喵！喵的非常好听！");
    }
}
```

### 方法的重载

重载发生在同一个类上，而重写发生在不同类上。

```java
public class Calculator {
    // 重载：参数个数不同
    public int add(int a, int b) {
        return a + b;
    }

    // 重载：参数个数不同
    public int add(int a, int b, int c) {
        return a + b + c;
    }

    // 重载：参数类型不同
    public double add(double a, double b) {
        return a + b;
    }

    // 重载：参数顺序不同
    public String add(String a, int b) {
        return a + b;
    }
}
```

调用时会自动匹配：

```java
Calculator calc = new Calculator();

calc.add(1, 2);          // 调用 add(int, int)
calc.add(1, 2, 3);       // 调用 add(int, int, int)
calc.add(1.5, 2.3);      // 调用 add(double, double)
calc.add("sum=", 10);    // 调用 add(String, int)
```

| 对比项 | 重载 | 重写 |
| --- | --- | --- |
| 发生位置 | 同一个类中 | 子类和父类之间 |
| 方法名 | 相同 | 相同 |
| 参数列表 | 必须不同 | 必须相同 |
| 返回值 | 不能作为重载依据 | 要兼容父类方法 |
| 典型注解 | 无 | `@Override` |

### 继承中的构造方法

子类构造方法中会先调用父类的构造方法，即使不写 `super()` 也会默认调用。

```java
class Person {
    private String name;
    private int age;

    public Person() {
        System.out.println("父类无参");
    }

    // getter/setter 省略
}

class Student extends Person {
    private double score;

    public Student() {
        // super(); // 调用父类无参，默认就存在，可以不写，必须在第一行
        System.out.println("子类无参");
    }

    public Student(double score) {
        // super(); // 调用父类无参，默认就存在，可以不写，必须在第一行
        this.score = score;
        System.out.println("子类有参");
    }
}
```

在子类中也可以调用父类的有参构造：

```java
class Person {
    private String name = "凤姐";
    private int age = 20;

    public Person() {
        System.out.println("父类无参");
    }

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // getter/setter 省略
}

class Student extends Person {
    private double score = 100;

    public Student() {
        // super(); // 调用父类无参构造方法，默认就存在，可以不写，必须在第一行
        System.out.println("子类无参");
    }

    public Student(String name, int age, double score) {
        super(name, age); // 调用父类有参构造方法 Person(String name, int age) 初始化 name 和 age
        this.score = score;
        System.out.println("子类有参");
    }

    // getter/setter 省略
}
```

## 抽象类和接口

![抽象类和接口](/java-technical-docs/images/source/image-05.png)

### 抽象类

抽象类使用 `abstract` 修饰。抽象方法没有方法体，子类必须实现。

```java
abstract class Animal {
    // 抽象方法：子类必须实现
    abstract void makeSound();

    // 普通方法：子类直接继承
    void sleep() {
        System.out.println("睡觉");
    }
}

class Dog extends Animal {
    @Override
    void makeSound() {
        System.out.println("汪汪");
    }
}

class Cat extends Animal {
    @Override
    void makeSound() {
        System.out.println("喵喵");
    }
}
```

抽象类适合表达“共同父类 + 部分实现”。比如动物都能睡觉，但是不同动物叫声不同。

### 接口

接口使用 `interface` 定义，类使用 `implements` 实现接口。

```java
interface Flyable {
    void fly();
}

class Bird implements Flyable {
    public void fly() {
        System.out.println("鸟在飞");
    }
}

class Plane implements Flyable {
    public void fly() {
        System.out.println("飞机在飞");
    }
}
```

接口更适合描述“能力”。比如鸟和飞机不是同一个父类体系，但都具备“会飞”这个能力。

| 对比项 | 抽象类 | 接口 |
| --- | --- | --- |
| 关键词 | `abstract class` | `interface` |
| 继承/实现 | `extends` | `implements` |
| 数量限制 | 一个类只能继承一个直接父类 | 一个类可以实现多个接口 |
| 适合表达 | 是什么 | 能做什么 |

## 本章检查

- 能说清 `static` 变量为什么被所有对象共享。
- 能写出私有构造方法的工具类。
- 能区分静态方法和非静态方法的访问范围。
- 能写出 `extends` 继承格式。
- 能用 `this` 和 `super` 区分当前类成员和父类成员。
- 能区分方法重写和方法重载。
- 能说明子类构造方法为什么会先调用父类构造方法。
- 能写出抽象类和接口的基本示例。
