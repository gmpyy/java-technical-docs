---
title: "请求参数、DI 与 MyBatis"
description: "GET/POST/Header/Path 参数接收、分层结构、依赖注入体系与 MyBatis"
outline: [2, 4]
---

# 请求参数、DI 与 MyBatis

这一章对应 `JAVA.md` 中“请求参数”“分层结构”“依赖注入体系”和“MyBatis”四块内容。这里保留原笔记的 8 种请求参数场景、完整 Controller 示例、分层流转说明和常用注解说明。

## 请求参数

### 1. GET query 参数拆分获取

请求示例：

```http
GET /api/query?id=123&name=tom
```

说明：

- 使用 `@RequestParam` 分别获取多个 query 参数。

```java
@GetMapping("/query")
public Map<String, Object> getByQueryParams(
        @RequestParam("id") Long id,
        @RequestParam("name") String name) {
    Map<String, Object> result = new HashMap<>();
    result.put("id", id);
    result.put("name", name);
    return result;
}
```

### 2. GET query 参数以 Map 获取

请求示例：

```http
GET /api/query-map?id=123&name=tom&city=shanghai
```

说明：

- 使用 `@RequestParam Map<String, String>` 一次性接收所有 query 参数。

```java
@GetMapping("/query-map")
public Map<String, Object> getByQueryMap(@RequestParam Map<String, String> params) {
    Map<String, Object> result = new HashMap<>(params);
    result.put("message", "收到所有查询参数");
    return result;
}
```

### 3. POST 请求体注册

请求示例：

```http
POST /api/register
Content-Type: application/json

{
  "username": "tom",
  "password": "123456"
}
```

说明：

- 使用 `@RequestBody` 接收 JSON 请求体。

```java
@PostMapping("/register")
public Map<String, Object> register(@RequestBody UserRegisterRequest request) {
    Map<String, Object> result = new HashMap<>();
    result.put("username", request.getUsername());
    result.put("password", request.getPassword());
    result.put("message", "注册成功");
    return result;
}
```

### 4. 请求头参数 Header

请求示例：

```http
GET /api/header-token
token: abc123
```

说明：

- 使用 `@RequestHeader("token")` 获取请求头参数。

```java
@GetMapping("/header-token")
public Map<String, Object> getByHeader(@RequestHeader("token") String token) {
    Map<String, Object> result = new HashMap<>();
    result.put("token", token);
    result.put("message", "从请求头获取 token");
    return result;
}
```

### 5. 路径参数 Path Variable

请求示例：

```http
GET /api/users/1
```

说明：

- 使用 `@PathVariable("userId")` 获取路径参数。

```java
@GetMapping("/users/{userId}")
public Map<String, Object> getByPath(@PathVariable("userId") Long userId) {
    Map<String, Object> result = new HashMap<>();
    result.put("userId", userId);
    result.put("message", "路径参数示例");
    return result;
}
```

### 6. 某参数可不传

请求示例：

```http
GET /api/optional
GET /api/optional?name=tom
```

说明：

- 使用 `required = false` 让参数可选。

```java
@GetMapping("/optional")
public Map<String, Object> optionalParams(
        @RequestParam(value = "name", required = false) String name,
        @RequestParam(value = "age", required = false) Integer age) {
    Map<String, Object> result = new HashMap<>();
    result.put("name", name);
    result.put("age", age);
    return result;
}
```

### 7. 某参数不传使用默认值

请求示例：

```http
GET /api/optional
```

说明：

- 使用 `defaultValue = "18"` 指定默认值。

```java
@GetMapping("/optional")
public Map<String, Object> optionalParams(
        @RequestParam(value = "name", required = false) String name,
        @RequestParam(value = "age", required = false, defaultValue = "18") Integer age) {
    Map<String, Object> result = new HashMap<>();
    result.put("name", name);
    result.put("age", age);
    result.put("message", "参数可选与默认值");
    return result;
}
```

### 8. 简洁写法

请求示例：

```http
GET /api/simple?id=1&name=tom
```

说明：

- 参数名与 query 参数一致时，可省略 `@RequestParam` 注解。

```java
@GetMapping("/simple")
public Map<String, Object> simpleParams(Long id, String name) {
    Map<String, Object> result = new HashMap<>();
    result.put("id", id);
    result.put("name", name);
    result.put("message", "简洁写法");
    return result;
}
```

![请求参数示例](/images/source/image-13.png)

## 完整请求参数示例

源笔记中的完整 Controller 示例整理如下：

```java
package com.study.study1.controller;

import java.util.HashMap;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class RequestDemoController {

    @GetMapping("/query")
    public Map<String, Object> getByQueryParams(
            @RequestParam("id") Long id,
            @RequestParam("name") String name) {
        Map<String, Object> result = new HashMap<>();
        result.put("id", id);
        result.put("name", name);
        return result;
    }

    @GetMapping("/query-map")
    public Map<String, Object> getByQueryMap(@RequestParam Map<String, String> params) {
        Map<String, Object> result = new HashMap<>(params);
        result.put("message", "收到所有查询参数");
        return result;
    }

    @PostMapping("/register")
    public Map<String, Object> register(@RequestBody UserRegisterRequest request) {
        Map<String, Object> result = new HashMap<>();
        result.put("username", request.getUsername());
        result.put("password", request.getPassword());
        result.put("message", "注册成功");
        return result;
    }

    @GetMapping("/header-token")
    public Map<String, Object> getByHeader(@RequestHeader("token") String token) {
        Map<String, Object> result = new HashMap<>();
        result.put("token", token);
        result.put("message", "从请求头获取 token");
        return result;
    }

    @GetMapping("/users/{userId}")
    public Map<String, Object> getByPath(@PathVariable("userId") Long userId) {
        Map<String, Object> result = new HashMap<>();
        result.put("userId", userId);
        result.put("message", "路径参数示例");
        return result;
    }

    @GetMapping("/optional")
    public Map<String, Object> optionalParams(
            @RequestParam(value = "name", required = false) String name,
            @RequestParam(value = "age", required = false, defaultValue = "18") Integer age) {
        Map<String, Object> result = new HashMap<>();
        result.put("name", name);
        result.put("age", age);
        result.put("message", "参数可选与默认值");
        return result;
    }

    @GetMapping("/simple")
    public Map<String, Object> simpleParams(Long id, String name) {
        Map<String, Object> result = new HashMap<>();
        result.put("id", id);
        result.put("name", name);
        result.put("message", "简洁写法");
        return result;
    }

    public static class UserRegisterRequest {
        private String username;
        private String password;

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
    }
}
```

## 分层结构

常见分层：

- `controller`：接口入口，负责接收参数与返回结果。
- `service`：业务逻辑层，负责组合数据与流程编排。
- `repository`：数据访问层，负责与数据库或存储交互。
- `model`
  - `dto`：请求数据结构（前端传入）。
  - `entity`：持久化对象（数据库表映射）。
  - `vo`：返回给前端的结构。

流程示例：

```text
前端请求
  -> DTO（请求体映射）
  -> Controller
  -> Service
  -> Repository
  -> Entity（持久化对象）
  -> Repository 返回 Entity
  -> Service 组装 VO
  -> Controller 返回 VO
  -> 前端
```

补充说明：

- DTO / VO 是数据结构，不是“流经”节点，而是在节点之间传递的对象。
- Entity 通常在 Service 与 Repository 之间使用。
- Controller 只负责入参 / 出参转换与调用 Service。

## 依赖注入体系

Spring 的核心原则：你声明依赖，容器负责创建与装配。

- **加入容器**：`@Controller`、`@Service`、`@Repository`、`@Component`、`@Configuration`、`@Bean`
- **取出注入**：`@Autowired`、`@Qualifier`、`@Value`
- **启动相关**：`@Configuration`、`@EnableAutoConfiguration`、`@ComponentScan`

### `@Controller`

- **作用**：标记控制层组件，处理 Web 请求。
- **结果**：类会被扫描并注册为 Bean。

```java
@Controller
public class UserController {
    // 处理请求的入口
}
```

实际 REST 接口中更常用 `@RestController`，它相当于 `@Controller` 加 `@ResponseBody`。

### `@Service`

- **作用**：标记业务层组件。
- **结果**：类会被注册为 Bean，通常用于业务逻辑。

```java
@Service
public class RequestDemoService {
    // 业务逻辑
}
```

### `@Repository`

- **作用**：标记持久层组件（DAO / Repository）。
- **结果**：类会被注册为 Bean，并具备数据库异常转换能力。

```java
@Repository
public class UserRepository {
    // 数据访问逻辑
}
```

### `@Component`

- **作用**：通用组件，常用于工具类或通用逻辑。
- **结果**：类会被注册为 Bean。

```java
@Component
public class TokenUtil {
    public String createToken(String userId) {
        return "token-" + userId;
    }
}
```

### `@Configuration`

- **作用**：配置类，声明 Spring 的各种配置。
- **结果**：Spring Boot 启动时会自动执行并加载其中的 Bean。

```java
@Configuration
public class AppConfig {
    // 放置各种配置
}
```

### `@Bean`

- **作用**：标记一个方法，把它的返回值注册为 Bean。
- **结果**：方法的返回对象被加入容器。
- **注意**：一般配合 `@Configuration` 使用。

```java
import java.util.HashMap;
import java.util.Map;

@Configuration
public class AppConfig {

    @Bean
    public Map<String, String> appMeta() {
        Map<String, String> meta = new HashMap<>();
        meta.put("app", "study1");
        return meta;
    }
}
```

### `@Autowired`

- **作用**：根据类型自动从容器中注入依赖。
- **行为**：如果是类对象就创建并注入，如果是值类型则直接赋值。

```java
@Service
public class UserBizService {

    @Autowired
    private RequestDemoService requestDemoService;
}
```

::: tip 建议
实际项目更推荐构造器注入，依赖关系更明确，也更利于单元测试。
:::

### `@Value`

- **作用**：从配置文件中注入具体值，如 `application.yml` 或 `application.properties`。

```java
@Component
public class AppInfo {

    @Value("${app.name}")
    private String appName;
}
```

### `@Qualifier`

- **作用**：当存在多个同类型 Bean 时，指定注入哪一个。

```java
@Service
public class ReportService {

    @Autowired
    @Qualifier("pdfExporter")
    private Exporter exporter;
}
```

### `@SpringBootApplication`

`@SpringBootApplication` 实际上由三个注解组合而成：

```text
@Configuration + @EnableAutoConfiguration + @ComponentScan
```

```java
@SpringBootApplication
public class Study1Application {
    public static void main(String[] args) {
        SpringApplication.run(Study1Application.class, args);
    }
}
```

### `@EnableAutoConfiguration`

- **作用**：开启 Spring Boot 的自动配置机制，根据依赖自动装配 Bean。

```java
@SpringBootApplication
@EnableAutoConfiguration
public class Study1Application {
    public static void main(String[] args) {
        SpringApplication.run(Study1Application.class, args);
    }
}
```

通常不需要单独写 `@EnableAutoConfiguration`，因为 `@SpringBootApplication` 已经包含它。

### `@ComponentScan`

- **作用**：指定扫描范围，把指定包下的组件加入容器。

```java
@SpringBootApplication
@ComponentScan(basePackages = {"com.study.study1", "com.thirdparty.lib"})
public class Study1Application {
    public static void main(String[] args) {
        SpringApplication.run(Study1Application.class, args);
    }
}
```

## MyBatis

MyBatis 一般在 `repository` 层使用，用来写 SQL 语句从数据库中获取数据。

```java
@Mapper
public interface UserRepository {
    @Select("""
            SELECT id, username, password, email
            FROM users
            WHERE id = #{id}
            """)
    UserEntity findById(@Param("id") Long id);
}
```

常见注意点：

- `@Mapper` 表示这是 MyBatis Mapper 接口。
- `@Select` 可以直接写查询 SQL。
- `#{id}` 表示绑定方法参数。
- `@Param("id")` 用于给参数命名，复杂 SQL 中很常见。
- 简单 SQL 可以用注解，复杂 SQL 更适合放到 XML。

## 本章检查

- 能写出 8 种常见请求参数接收方式。
- 能说明 `@RequestParam`、`@RequestBody`、`@RequestHeader`、`@PathVariable` 的区别。
- 能看懂完整的 `RequestDemoController`。
- 能说清 Controller、Service、Repository、DTO、Entity、VO 的关系。
- 能区分加入容器和取出注入相关注解。
- 能说明 `@SpringBootApplication` 的组合含义。
- 能写出一个基础 MyBatis Mapper 查询。
