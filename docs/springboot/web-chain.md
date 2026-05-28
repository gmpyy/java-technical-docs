---
title: "Filter、Interceptor 与 CORS"
description: "过滤器、拦截器、WebMvcConfigurer、日志拦截与跨域设置"
outline: [2, 4]
---

# Filter、Interceptor 与 CORS

这一章对应 `JAVA.md` 中“拦截器，过滤器以及全局 MVC 配置”和“cors 跨域设置”两部分。这里保留原图、过滤器示例、登录验证过滤器、传统 XML 配置、拦截器示例、日志拦截器、`WebMvcConfigurer` 注册方式，以及 CORS 的 Filter / Interceptor 两种写法。

## 拦截器、过滤器以及全局 MVC 配置

![Filter 与 Interceptor 图 1](/images/source/image-14.png)

![Filter 与 Interceptor 图 2](/images/source/image-15.png)

![Filter 与 Interceptor 图 3](/images/source/image-16.png)

![Filter 与 Interceptor 图 4](/images/source/image-17.png)

![Filter 与 Interceptor 图 5](/images/source/image-18.png)

简化链路：

```text
客户端请求
  -> Filter（Servlet 容器层）
  -> DispatcherServlet
  -> Interceptor.preHandle（Spring MVC 层）
  -> Controller
  -> Interceptor.postHandle
  -> Interceptor.afterCompletion
  -> 响应返回
```

## 过滤器代码示例

### 创建自定义过滤器

```java
package com.study.study1.filter;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * 字符编码过滤器
 * 使用 @WebFilter 注解配置
 */
@WebFilter(urlPatterns = "/*")  // 拦截所有请求
public class EncodingFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        // 过滤器初始化时调用
        System.out.println("EncodingFilter 初始化");
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {

        // 1. 请求预处理
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        // 设置字符编码
        httpRequest.setCharacterEncoding("UTF-8");
        httpResponse.setCharacterEncoding("UTF-8");
        httpResponse.setContentType("text/html;charset=UTF-8");

        System.out.println("【Filter】请求预处理: " + httpRequest.getRequestURI());

        // 2. 放行请求（重要！必须调用）
        chain.doFilter(request, response);

        // 3. 响应后处理（在请求处理完成后执行）
        System.out.println("【Filter】响应后处理完成");
    }

    @Override
    public void destroy() {
        // 过滤器销毁时调用
        System.out.println("EncodingFilter 销毁");
    }
}
```

### 登录验证过滤器

```java
package com.study.study1.filter;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

/**
 * 登录验证过滤器
 * 拦截需要登录才能访问的页面
 */
@WebFilter(urlPatterns = "/admin/*")  // 只拦截 /admin/ 下的请求
public class LoginFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        HttpSession session = httpRequest.getSession(false);  // 不创建新 session

        // 检查是否已登录
        boolean isLoggedIn = (session != null &&
                             session.getAttribute("user") != null);

        // 检查是否是登录请求
        boolean isLoginRequest = httpRequest.getRequestURI().contains("/login");

        if (isLoggedIn || isLoginRequest) {
            // 已登录或登录请求，放行
            chain.doFilter(request, response);
        } else {
            // 未登录，重定向到登录页面
            httpResponse.sendRedirect(httpRequest.getContextPath() + "/login");
        }
    }
}
```

### 传统 XML 配置方式

不使用注解时，可以通过 `web.xml` 配置。

```java
public class TraditionalFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        // 处理逻辑
        chain.doFilter(request, response);
    }
}
```

`web.xml` 配置：

```xml
<filter>
    <filter-name>encodingFilter</filter-name>
    <filter-class>com.study.study1.filter.EncodingFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>encodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

## 拦截器代码示例

### 创建自定义拦截器

```java
package com.study.study1.interceptor;

import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * 登录检查拦截器
 * 用于拦截需要登录才能访问的请求
 */
public class LoginInterceptor implements HandlerInterceptor {

    /**
     * Controller 执行前调用
     * @return true = 放行，false = 拦截（不执行 Controller）
     */
    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) throws Exception {

        System.out.println("【Interceptor】preHandle 执行: " + request.getRequestURI());

        // 获取 session，不自动创建
        HttpSession session = request.getSession(false);
        Object user = session != null ? session.getAttribute("user") : null;

        if (user != null) {
            // 已登录，放行
            return true;
        } else {
            // 未登录，重定向到登录页
            response.sendRedirect(request.getContextPath() + "/login");
            return false;  // 拦截请求，不执行 Controller
        }
    }

    /**
     * Controller 执行后，视图渲染前调用
     */
    @Override
    public void postHandle(HttpServletRequest request,
                           HttpServletResponse response,
                           Object handler,
                           ModelAndView modelAndView) throws Exception {

        System.out.println("【Interceptor】postHandle 执行: " + request.getRequestURI());

        // 可以在此修改 ModelAndView，比如添加公共数据
        if (modelAndView != null) {
            modelAndView.addObject("timestamp", System.currentTimeMillis());
        }
    }

    /**
     * 整个请求完成后调用（无论成功或异常）
     */
    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler,
                                Exception ex) throws Exception {

        System.out.println("【Interceptor】afterCompletion 执行: " + request.getRequestURI());

        // 可以在此记录日志、清理资源等
        if (ex != null) {
            System.out.println("【Interceptor】异常信息: " + ex.getMessage());
        }
    }
}
```

### 日志拦截器

```java
package com.study.study1.interceptor;

import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * 请求日志拦截器
 * 记录请求的处理时间
 */
public class LoggingInterceptor implements HandlerInterceptor {

    // 使用 ThreadLocal 存储开始时间
    private static final ThreadLocal<Long> START_TIME = new ThreadLocal<>();

    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) throws Exception {

        long startTime = System.currentTimeMillis();
        START_TIME.set(startTime);

        System.out.println("========== 请求开始 ==========");
        System.out.println("URL: " + request.getRequestURL());
        System.out.println("Method: " + request.getMethod());
        System.out.println("IP: " + request.getRemoteAddr());

        return true;  // 放行
    }

    @Override
    public void postHandle(HttpServletRequest request,
                           HttpServletResponse response,
                           Object handler,
                           org.springframework.web.servlet.ModelAndView modelAndView) throws Exception {

        long startTime = START_TIME.get();
        long endTime = System.currentTimeMillis();
        long executeTime = endTime - startTime;

        System.out.println("========== 请求处理完成 ==========");
        System.out.println("处理时间: " + executeTime + "ms");
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler,
                                Exception ex) throws Exception {

        // 清理 ThreadLocal
        START_TIME.remove();

        System.out.println("========== 请求完全结束 ==========");
        System.out.println("状态码: " + response.getStatus());
    }
}
```

## 拦截器配置：全局 MVC 文件 WebMvcConfigurer

通过 `WebMvcConfigurer` 注册拦截器：

```java
package com.study.study1.config;

import com.study.study1.interceptor.LoginInterceptor;
import com.study.study1.interceptor.LoggingInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {

        // 注册日志拦截器 - 拦截所有请求
        registry.addInterceptor(new LoggingInterceptor())
                .addPathPatterns("/**")
                .excludePathPatterns("/static/**", "/login", "/error");

        // 注册登录拦截器 - 只拦截需要登录的请求
        registry.addInterceptor(new LoginInterceptor())
                .addPathPatterns("/admin/**", "/user/profile")
                .excludePathPatterns("/login", "/register", "/static/**");
    }
}
```

## CORS 跨域设置

浏览器跨域请求会受到同源策略限制。后端可以通过设置响应头来允许指定来源访问接口。

### 1. 使用过滤器 Filter 实现 CORS

过滤器位于 Servlet 容器层，对所有请求生效，适合做全局跨域处理。

#### 示例代码

```java
import java.io.IOException;
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;

@Component
public class CorsFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        String origin = req.getHeader("Origin");
        if (origin != null && !origin.isEmpty()) {
            res.setHeader("Access-Control-Allow-Origin", origin);
            res.setHeader("Vary", "Origin");
        }
        res.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS");
        res.setHeader("Access-Control-Allow-Headers", "Content-Type,Authorization");
        // 如果需要 cookie 的话，就要添加这个字段
        res.setHeader("Access-Control-Allow-Credentials", "true");
        res.setHeader("Access-Control-Max-Age", "3600");

        // 预检请求的处理，预检请求返回状态码 200 即可，无需执行后续业务逻辑
        if ("OPTIONS".equalsIgnoreCase(req.getMethod())) {
            res.setStatus(HttpServletResponse.SC_OK);
            return;
        }

        chain.doFilter(request, response);
    }
}
```

### 2. 使用拦截器 Interceptor 实现 CORS

拦截器运行在 Spring MVC 层，可以按路径控制，便于与业务拦截逻辑统一管理。

#### 示例代码

```java
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class CorsInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type,Authorization");
        response.setHeader("Access-Control-Allow-Credentials", "true");
        response.setHeader("Access-Control-Max-Age", "3600");

        if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
            response.setStatus(HttpServletResponse.SC_OK);
            return false;
        }
        return true;
    }
}
```

注册 CORS 拦截器：

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    private final CorsInterceptor corsInterceptor;

    @Autowired
    public WebMvcConfig(CorsInterceptor corsInterceptor) {
        this.corsInterceptor = corsInterceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(corsInterceptor).addPathPatterns("/**");
    }
}
```

::: warning 生产环境注意
如果需要携带 Cookie 或认证信息，不建议使用完全开放的跨域策略。生产环境应限制为可信前端域名。
:::

## 本章检查

- 能说出 Filter 和 Interceptor 分别属于哪一层。
- 能写出 `chain.doFilter(request, response)`，并知道它是放行请求的关键。
- 能写出登录验证过滤器。
- 能说出 `preHandle`、`postHandle`、`afterCompletion` 的执行时机。
- 能用 `WebMvcConfigurer` 注册多个拦截器。
- 能用 Filter 或 Interceptor 实现 CORS，并知道预检请求 `OPTIONS` 如何处理。
