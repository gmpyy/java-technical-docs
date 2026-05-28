---
title: "项目结构与分层"
description: "Spring Boot 目录结构、resources 内容、DTO、entity、VO 与各层职责"
outline: [2, 3]
---

# 项目结构与分层

Spring Boot 项目最重要的不是目录看起来多，而是职责边界清楚：请求入口、业务流程、数据访问、数据库映射和返回结构要分开。

## 项目结构概览

```text
study1
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com/study/study1
│   │   │       ├── controller
│   │   │       ├── service
│   │   │       ├── repository
│   │   │       ├── entity
│   │   │       ├── dto
│   │   │       ├── vo
│   │   │       └── config
│   │   └── resources
│   └── test
└── pom.xml
```

## 核心目录说明

| 目录 | 职责 |
| --- | --- |
| `controller` | 处理 HTTP 请求，接收参数，返回结果 |
| `service` | 编写业务逻辑，组织事务和调用流程 |
| `repository` / `mapper` | 数据访问层，操作数据库 |
| `entity` | 数据库表映射对象 |
| `dto` | 请求数据结构 |
| `vo` | 返回给前端的数据结构 |
| `config` | 全局配置、拦截器注册、Bean 声明 |

## 推荐扩展结构

当项目复杂后，可以增加更明确的包：

```text
com/example/app
├── common       # 通用响应、异常、常量
├── exception    # 业务异常和全局异常处理
├── security     # 登录、JWT、权限
├── task         # 定时任务
└── util         # 工具类
```

## 各层职责

### Controller

Controller 面向 HTTP，负责参数接收、基础校验和响应包装，不应该堆复杂业务。

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

Service 表达业务流程，是事务和复杂逻辑最常出现的位置。

```java
@Service
public class UserService {
    public UserVO findDetail(Long id) {
        // 查询用户、组装返回对象、处理业务规则
        return new UserVO();
    }
}
```

### Repository / Mapper

数据访问层只关心数据读写，不应混入 HTTP 或页面展示逻辑。

## DTO / entity / VO

| 类型 | 面向边界 | 典型职责 |
| --- | --- | --- |
| DTO | 前端请求 | 接收注册、登录、分页查询等入参 |
| entity | 数据库 | 与表结构对应，通常不直接暴露给前端 |
| VO | 前端响应 | 只返回前端需要展示的数据 |

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

`resources` 常放配置和静态资源：

- `application.yml`：项目配置。
- `mapper/*.xml`：MyBatis XML。
- `static/`：静态资源。
- `templates/`：模板页面。

```yaml
server:
  port: 8080

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/study
```

