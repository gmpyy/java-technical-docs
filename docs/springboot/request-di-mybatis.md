---
title: "请求参数、DI 与 MyBatis"
description: "GET/POST/Header/Path 参数接收、常用注解、依赖注入体系与 MyBatis"
outline: [2, 3]
---

# 请求参数、DI 与 MyBatis

Spring Boot Web 开发的主线是：Controller 接收请求参数，Service 处理业务，Mapper 或 Repository 访问数据库，最终返回 VO。

## GET query 参数拆分获取

```java
@GetMapping("/users")
public List<UserVO> list(@RequestParam Long id,
                         @RequestParam String name) {
    return userService.search(id, name);
}
```

请求示例：

```http
GET /api/users?id=1&name=tom
```

## GET query 参数以 Map 获取

```java
@GetMapping("/users/map")
public Map<String, String> query(@RequestParam Map<String, String> params) {
    return params;
}
```

这种写法适合参数不固定的场景，但业务接口更建议用明确字段。

## POST 请求体注册

```java
@PostMapping("/register")
public UserVO register(@RequestBody RegisterDTO dto) {
    return userService.register(dto);
}
```

```java
public class RegisterDTO {
    private String phone;
    private String password;
    private String nickname;
}
```

## 请求头参数 Header

请求头常用于 Token、客户端版本、traceId 等元信息。

```java
@GetMapping("/me")
public UserVO me(@RequestHeader("Authorization") String authorization) {
    return userService.currentUser(authorization);
}
```

## 路径参数 Path Variable

路径参数常用于资源 ID。

```java
@GetMapping("/users/{id}")
public UserVO detail(@PathVariable Long id) {
    return userService.findDetail(id);
}
```

## 可选参数与默认值

```java
@GetMapping("/optional")
public String optional(@RequestParam(required = false) String name,
                       @RequestParam(defaultValue = "18") Integer age) {
    return name + ":" + age;
}
```

`@RequestParam` 可以通过 `required = false` 让参数可选，也可以通过 `defaultValue` 设置默认值。

## 依赖注入体系

Spring 会扫描组件，把对象放进容器，然后在需要的位置注入。

| 注解 | 作用 |
| --- | --- |
| `@Controller` | 标记 MVC Controller |
| `@Service` | 标记业务层组件 |
| `@Repository` | 标记数据访问层组件 |
| `@Component` | 通用组件 |
| `@Configuration` | 配置类 |
| `@Bean` | 手动注册 Bean |
| `@Autowired` | 按类型注入依赖 |
| `@Value` | 注入配置值 |
| `@Qualifier` | 按名称指定注入对象 |

```java
@Service
public class OrderService {
    private final OrderMapper orderMapper;

    public OrderService(OrderMapper orderMapper) {
        this.orderMapper = orderMapper;
    }
}
```

::: tip 建议
项目中优先使用构造器注入，依赖更明确，也更容易测试。
:::

## SpringBootApplication

`@SpringBootApplication` 通常包含三层含义：

- `@SpringBootConfiguration`
- `@EnableAutoConfiguration`
- `@ComponentScan`

```java
@SpringBootApplication
public class StudyApplication {
    public static void main(String[] args) {
        SpringApplication.run(StudyApplication.class, args);
    }
}
```

## MyBatis

MyBatis 常用 Mapper 接口承接 SQL 查询。

```java
@Mapper
public interface UserMapper {
    @Select("select id, phone, nickname from user where id = #{id}")
    UserEntity findById(Long id);
}
```

XML 写法适合复杂 SQL：

```xml
<select id="findByPhone" resultType="com.example.UserEntity">
  select id, phone, nickname
  from user
  where phone = #{phone}
</select>
```

