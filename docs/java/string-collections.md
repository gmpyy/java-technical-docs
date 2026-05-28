---
title: "字符串与集合"
description: "字符串比较、StringBuilder、StringJoiner、ArrayList、数组、List、Set、Map 与枚举"
outline: [2, 4]
---

# 字符串与集合

这一章对应 `JAVA.md` 中“字符串的比较”到“枚举定义”的内容。这里保留源笔记的常用 API、示例代码和集合操作清单。

## 字符串的比较

### `==` 号的作用

- 比较基本数据类型：比较的是具体的值。
- 比较引用数据类型：比较的是对象地址值。

```java
int a = 10;
int b = 10;
System.out.println(a == b); // true

String s1 = new String("java");
String s2 = new String("java");
System.out.println(s1 == s2); // false，比较的是地址
```

### `equals` 方法的作用

`equals` 用于比较两个字符串内容是否相同，区分大小写。

```java
public boolean equals(String s)
```

用户输入一个字符串时，如果要比较内容，应该使用 `equals` 方法，因为输入的字符串通常是对象引用，直接用 `==` 比较的是地址。

```java
String input = new String("admin");

System.out.println(input == "admin");      // 不推荐
System.out.println(input.equals("admin")); // 推荐
```

如果担心变量为 `null`，可以把常量写在前面：

```java
if ("admin".equals(input)) {
    System.out.println("登录管理员账号");
}
```

## StringBuilder

`StringBuilder` 可以看成是一个容器，创建之后里面的内容是可变的。

当我们在拼接字符串和反转字符串的时候，会使用到 `StringBuilder`。

### 基本使用

```java
public class StringBuilderDemo3 {
    public static void main(String[] args) {
        // 1. 创建对象
        StringBuilder sb = new StringBuilder("abc");

        // 2. 添加元素
        /*
        sb.append(1);
        sb.append(2.3);
        sb.append(true);
        */

        // 反转
        sb.reverse();

        // 获取长度
        int len = sb.length();
        System.out.println(len);

        // 打印
        // 普及：
        // 因为 StringBuilder 是 Java 已经写好的类，
        // Java 在底层对它做了一些特殊处理。
        // 打印对象不是地址值而是属性值。
        // toString 变回字符串。
        String str = sb.toString();
        System.out.println(str);
    }
}
```

常见链式拼接：

```java
String result = new StringBuilder()
        .append("user:")
        .append(1001)
        .append(":")
        .append("active")
        .toString();
```

## 字符串操作

源笔记中的字符串常用操作清单：

1. 判断相等：`equals`
2. 判断空字符串：`isEmpty` 或者 `equals("")`
3. 分割为数组：`split`
4. 正则匹配：`matches`
5. 替换操作：`replace` 替换所有但不支持正则，`replaceAll` 也替换所有并且支持正则
6. 字符串位置：`indexOf`
7. 简单拼接：`+`
8. 链式调用拼接：`concat`
9. 字符之间插入字符串拼接：`join`
10. 模板字符串：`String.format`

示例：

```java
public class StringApiDemo {
    public static void main(String[] args) {
        String text = "java,spring,redis";

        System.out.println(text.equals("java"));
        System.out.println(text.isEmpty());

        String[] parts = text.split(",");
        for (String part : parts) {
            System.out.println(part);
        }

        System.out.println("13800000000".matches("^1[3-9]\\d{9}$"));
        System.out.println(text.replace("java", "Java"));
        System.out.println(text.indexOf("spring"));
        System.out.println("Hello ".concat("Java"));
        System.out.println(String.join("/", "api", "users", "1001"));
        System.out.println(String.format("name=%s, age=%d", "Tom", 18));
    }
}
```

## StringJoiner

`StringJoiner` 可以指定分隔符，也可以指定开始符号和结束符号。

### 基本使用

只指定中间的间隔符号：

```java
import java.util.StringJoiner;

public class StringJoinerDemo1 {
    public static void main(String[] args) {
        // 1. 创建一个对象，并指定中间的间隔符号
        StringJoiner sj = new StringJoiner("---");

        // 2. 添加元素
        sj.add("aaa").add("bbb").add("ccc");

        // 3. 打印结果
        System.out.println(sj); // aaa---bbb---ccc
    }
}
```

指定分隔符号、开始符号、结束符号：

```java
import java.util.StringJoiner;

public class StringJoinerDemo2 {
    public static void main(String[] args) {
        // 1. 创建对象，指定分隔符号、开始符号、结束符号
        StringJoiner sj = new StringJoiner(", ", "[", "]");

        // 2. 添加元素
        sj.add("aaa").add("bbb").add("ccc");

        int len = sj.length();
        System.out.println(len); // 15

        // 3. 打印
        System.out.println(sj); // [aaa, bbb, ccc]

        String str = sj.toString();
        System.out.println(str); // [aaa, bbb, ccc]
    }
}
```

## ArrayList 集合

![ArrayList 集合](/images/source/image-04.png)

### 成员方法

常见成员方法：

| 方法 | 说明 |
| --- | --- |
| `add(E e)` | 添加元素 |
| `remove(Object o)` | 删除指定元素，返回删除是否成功 |
| `remove(int index)` | 删除指定索引处的元素，返回被删除的元素 |
| `set(int index, E element)` | 修改指定索引处的元素，返回被修改的元素 |
| `get(int index)` | 返回指定索引处的元素 |
| `size()` | 返回集合中的元素个数 |

### 示例代码

```java
import java.util.ArrayList;

public class ArrayListDemo02 {
    public static void main(String[] args) {
        // 创建集合
        ArrayList<String> array = new ArrayList<String>();

        // 添加元素
        array.add("hello");
        array.add("world");
        array.add("java");

        // public boolean remove(Object o)：删除指定的元素，返回删除是否成功
        // System.out.println(array.remove("world"));
        // System.out.println(array.remove("javaee"));

        // public E remove(int index)：删除指定索引处的元素，返回被删除的元素
        // System.out.println(array.remove(1));

        // IndexOutOfBoundsException
        // System.out.println(array.remove(3));

        // public E set(int index, E element)：修改指定索引处的元素，返回被修改的元素
        // System.out.println(array.set(1, "javaee"));

        // IndexOutOfBoundsException
        // System.out.println(array.set(3, "javaee"));

        // public E get(int index)：返回指定索引处的元素
        // System.out.println(array.get(0));
        // System.out.println(array.get(1));
        // System.out.println(array.get(2));
        // System.out.println(array.get(3)); // 自己测试

        // public int size()：返回集合中的元素的个数
        System.out.println(array.size());

        // 输出集合
        System.out.println("array:" + array);
    }
}
```

## 数组、List、Set

### 数组

数组长度固定，一般业务开发中不如集合灵活。

直接声明一个里面有 `1`、`2`、`3` 三个元素的数组：

```java
int[] arr = {1, 2, 3};
```

数组操作：

- 取值和改值：通过下标实现。
- 遍历：`for` 和增强 `for`。
- 转为 Stream 后：可以使用 `forEach`。

```java
int[] arr = {1, 2, 3};

arr[0] = 10;
System.out.println(arr[0]);

for (int value : arr) {
    System.out.println(value);
}
```

### List

`List` 相当于前端的数组，长度不固定，常用实现类是 `ArrayList`。

List 操作：

- 增加、删除：`add`、`remove`、`clear`
- 遍历：`for`、增强 `for`、`forEach`、`iterator`
- 转为 Stream 后：`filter`、`map`、`sort`

```java
import java.util.ArrayList;
import java.util.List;

public class ListDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("java");
        list.add("redis");
        list.add("spring");

        list.remove("redis");

        list.forEach(System.out::println);
    }
}
```

### Set

`Set` 和 `List` 最大的区别就是：`Set` 中的元素唯一，其他用法和 `List` 差不多。

```java
import java.util.HashSet;
import java.util.Set;

public class SetDemo {
    public static void main(String[] args) {
        Set<String> set = new HashSet<>();
        set.add("java");
        set.add("java");
        set.add("redis");

        System.out.println(set.size()); // 2
    }
}
```

## Map 操作

### 种类

- `HashMap`：无序，顺序跟任何东西没有关系。
- `LinkedHashMap`：按照 `put` 的顺序排序，先 `put` 的在前面。
- `TreeMap`：升序，对 key 进行排序。

### 方法

- 新增：`put`
- 删除：`remove`
- 修改：`replace`
- 查询：`get`
- 清空：`clear`
- 获取所有 key：`keySet`
- 获取所有值：`values`
- 处理成键值对对象，每一个对象都有 key、value：`entrySet`
- 遍历：`for`、`forEach`
- 判断是否存在某个 key：`containsKey`

```java
import java.util.HashMap;
import java.util.Map;

public class MapDemo {
    public static void main(String[] args) {
        Map<String, Integer> scores = new HashMap<>();

        scores.put("Tom", 90);
        scores.put("Jerry", 95);
        scores.replace("Tom", 92);

        System.out.println(scores.get("Tom"));
        System.out.println(scores.containsKey("Jerry"));

        for (String key : scores.keySet()) {
            System.out.println(key + "=" + scores.get(key));
        }

        scores.forEach((key, value) -> System.out.println(key + ":" + value));
    }
}
```

## 枚举定义

枚举适合表示固定取值集合，例如订单状态。

```java
public enum OrderStatus {
    UNFINISH("未完成", "UNFINISH"),
    FINISH("完成", "FINISH"),
    FAIL("失败", "FAIL");

    public String name;
    public String code;

    OrderStatus(String name, String code) {
        this.name = name;
        this.code = code;
    }
}
```

实际项目中，如果不希望外部直接修改枚举字段，可以把字段改成 `private final`，再提供 getter。

```java
public enum SafeOrderStatus {
    UNFINISH("未完成", "UNFINISH"),
    FINISH("完成", "FINISH"),
    FAIL("失败", "FAIL");

    private final String name;
    private final String code;

    SafeOrderStatus(String name, String code) {
        this.name = name;
        this.code = code;
    }

    public String getName() {
        return name;
    }

    public String getCode() {
        return code;
    }
}
```

## 本章检查

- 能说清 `==` 和 `equals` 的区别。
- 能用 `StringBuilder` 做拼接、反转、转回字符串。
- 知道 `split`、`matches`、`replace`、`replaceAll`、`indexOf`、`concat`、`join`、`String.format` 的常见用途。
- 能用 `StringJoiner` 拼出带分隔符、前后缀的字符串。
- 能写出 `ArrayList` 的增删改查。
- 能区分数组、`List`、`Set` 和 `Map` 的使用场景。
- 能定义带字段和构造方法的枚举。
