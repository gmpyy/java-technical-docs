---
title: "字符串与集合"
description: "字符串比较、StringBuilder、StringJoiner、ArrayList、数组、List、Set、Map 与枚举"
outline: [2, 3]
---

# 字符串与集合

字符串和集合是 Java 日常开发里最常用的基础 API。学习时不要只背方法名，要知道它们适合什么场景。

## 字符串比较

`==` 比较的是引用地址，`equals` 比较的是内容。

```java
String a = new String("java");
String b = new String("java");

System.out.println(a == b);      // false
System.out.println(a.equals(b)); // true
```

::: warning 注意
判断字符串内容是否相等时，优先使用 `equals`。如果变量可能为 `null`，可以写成 `"java".equals(value)`。
:::

## StringBuilder

`StringBuilder` 适合频繁拼接字符串，避免产生过多临时字符串对象。

```java
public class StringBuilderDemo {
    public static void main(String[] args) {
        StringBuilder builder = new StringBuilder();
        builder.append("Java");
        builder.append(" ");
        builder.append("Docs");

        System.out.println(builder.toString());
    }
}
```

常见链式写法：

```java
String result = new StringBuilder()
        .append("user:")
        .append(1001)
        .append(":")
        .append("active")
        .toString();
```

## 字符串操作

| 方法 | 作用 |
| --- | --- |
| `matches` | 判断字符串是否匹配正则表达式 |
| `indexOf` | 查找子串第一次出现的位置 |
| `concat` | 拼接字符串 |
| `join` | 使用分隔符连接多个字符串 |

```java
String phone = "13800000000";
boolean valid = phone.matches("^1[3-9]\\d{9}$");

String path = String.join("/", "api", "users", "1001");
System.out.println(valid);
System.out.println(path);
```

## StringJoiner

`StringJoiner` 可以指定分隔符、前缀和后缀，适合生成结构化展示字符串。

```java
import java.util.StringJoiner;

StringJoiner joiner = new StringJoiner(", ", "[", "]");
joiner.add("Java");
joiner.add("Spring Boot");
joiner.add("Redis");

System.out.println(joiner); // [Java, Spring Boot, Redis]
```

## ArrayList

`ArrayList` 是基于数组实现的动态集合，适合按顺序保存对象。

```java
import java.util.ArrayList;

ArrayList<String> names = new ArrayList<>();
names.add("tom");
names.add("jerry");
names.remove("tom");

for (String name : names) {
    System.out.println(name);
}
```

常用成员方法：

| 方法 | 说明 |
| --- | --- |
| `add` | 添加元素 |
| `remove` | 删除元素 |
| `clear` | 清空集合 |
| `get` | 根据索引获取元素 |
| `set` | 修改指定位置的元素 |

## 数组、List、Set

| 结构 | 特点 | 适合场景 |
| --- | --- | --- |
| 数组 | 长度固定，访问快 | 固定数量的数据 |
| List | 有序，可重复 | 常规列表、分页结果 |
| Set | 无序，不重复 | 去重、成员判断 |

```java
Set<String> tags = new HashSet<>();
tags.add("java");
tags.add("redis");
tags.add("java");

System.out.println(tags.size()); // 2
```

## Map 操作

`Map` 保存键值对，常用于按 ID、名称或编码快速查找对象。

```java
Map<Long, String> userNames = new HashMap<>();
userNames.put(1L, "tom");
userNames.put(2L, "jerry");

String name = userNames.get(1L);
boolean exists = userNames.containsKey(2L);
```

## 枚举

枚举适合表示固定取值集合，例如订单状态、用户角色、消息类型。

```java
public enum OrderStatus {
    CREATED,
    PAID,
    CANCELLED
}
```

::: tip 使用建议
如果某个字段只能从一组固定值里选择，优先考虑枚举，而不是散落在代码里的字符串常量。
:::

