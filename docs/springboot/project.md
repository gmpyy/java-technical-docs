---
title: "项目结构与分层"
description: "Spring Boot 目录结构、核心目录、扩展结构、各层职责与 resources 内容"
outline: [2, 4]
---

# 项目结构与分层

这一章对应 `JAVA.md` 中 Spring Boot 开头的目录结构部分。这里保留原始目录树、两张配图、核心目录说明、推荐扩展结构、各层职责和 `resources` 目录内容。

## Spring Boot

Spring Boot 项目看起来目录不多，但后端项目真正重要的是职责边界：控制层处理请求，服务层处理业务，数据访问层操作数据库，配置类管理项目配置。

## 目录结构

![Spring Boot 目录结构](/java-technical-docs/images/source/image-11.png)

## 项目结构概览

```text
study1/                              # 项目根目录
├── src/
│   ├── main/                        # 主代码目录
│   │   ├── java/                    # Java 源代码
│   │   │   └── com/study/study1/    # 包结构（公司域名反写 + 项目名）
│   │   │       └── Study1Application.java  # 启动类
│   │   │
│   │   └── resources/               # 资源文件目录
│   │       └── application.properties       # 配置文件
│   │
│   └── test/                        # 测试代码目录
│       ├── java/                    # 测试源代码
│       │   └── com/study/study1/
│       │       └── Study1ApplicationTests.java
│       │
│       └── resources/               # 测试资源（可省略）
│
├── pom.xml                          # Maven 配置文件（依赖管理）
├── mvnw / mvnw.cmd                  # Maven 包装脚本（跨平台）
└── target/                          # 编译输出目录（自动生成）
```

## 核心目录说明

| 目录 | 作用 |
| --- | --- |
| `src/main/java` | 存放所有 Java 业务代码 |
| `src/main/resources` | 存放配置文件、静态资源、模板 |
| `src/test/java` | 存放单元测试 / 集成测试代码 |
| `pom.xml` | Maven 项目配置，定义依赖和构建插件 |

## 推荐的扩展结构

对于较大的项目，通常会在 `java` 目录下添加更多包：

```text
com/study/study1/
├── controller/      # 控制层（处理 HTTP 请求）
├── service/         # 业务逻辑层
├── repository/      # 数据访问层（DAO）
├── entity/          # 实体类（对应数据库表）
├── config/          # 配置类
└── dto/             # 数据传输对象
```

如果项目继续变复杂，也可以继续扩展：

```text
com/study/study1/
├── common/          # 通用响应、常量、工具对象
├── exception/       # 自定义异常、全局异常处理
├── mapper/          # MyBatis Mapper 接口
├── vo/              # 返回给前端的视图对象
├── task/            # 定时任务
└── util/            # 工具类
```

## 各层职责

- **Controller（控制层）**：接收用户请求，调用 Service 层，返回响应。
- **Service（服务层）**：处理业务逻辑。
- **Repository（持久层）**：与数据库交互。
- **Entity（实体类）**：对应数据库表的 Java 对象。
- **Config（配置类）**：应用配置 Bean。

### Controller

Controller 面向 HTTP 请求，负责接收参数、调用业务服务、返回结果。

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public UserVO detail(@PathVariable Long id) {
        return userService.findDetail(id);
    }
}
```

### Service

Service 面向业务流程，负责组织业务逻辑、事务和多个数据访问操作。

```java
@Service
public class UserService {
    public UserVO findDetail(Long id) {
        // 查询用户、判断业务规则、组装返回对象
        return new UserVO();
    }
}
```

### Repository / Mapper

Repository 或 Mapper 面向数据库，只负责数据读写，不应该混入 HTTP 请求处理或页面展示逻辑。

```java
@Repository
public class UserRepository {
    public UserEntity findById(Long id) {
        // 查询数据库
        return new UserEntity();
    }
}
```

### Entity、DTO、VO

| 类型 | 面向边界 | 作用 |
| --- | --- | --- |
| `DTO` | 请求入参 | 接收注册、登录、分页查询等前端传入的数据 |
| `entity` | 数据库 | 与数据库表结构对应 |
| `VO` | 响应结果 | 返回给前端展示的数据 |

```java
public class LoginDTO {
    private String phone;
    private String code;
}

public class UserEntity {
    private Long id;
    private String phone;
    private String password;
}

public class UserVO {
    private Long id;
    private String nickname;
}
```

## resources 目录内容

```text
src/main/resources/
├── application.properties      # 主配置文件
├── application.yml             # 或使用 YAML 格式
├── static/                     # 静态资源（CSS, JS, 图片）
└── templates/                  # 模板文件（Thymeleaf, FreeMarker 等）
```

![resources 目录内容](/java-technical-docs/images/source/image-12.png)

常见配置示例：

```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/study
    username: root
    password: root
```

## 本章检查

- 能说出 Spring Boot 项目的标准目录结构。
- 知道 `src/main/java`、`src/main/resources`、`src/test/java`、`pom.xml` 的作用。
- 能按 Controller、Service、Repository、Entity、Config、DTO 拆包。
- 能区分 DTO、entity、VO。
- 知道 `resources` 目录可以放配置文件、静态资源和模板。
