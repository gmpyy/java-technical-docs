---
title: "Filter、Interceptor 与 CORS"
description: "过滤器、拦截器、WebMvcConfigurer、日志拦截与跨域设置"
outline: [2, 3]
---

# Filter、Interceptor 与 CORS

请求进入 Spring Boot 应用后，可能先经过 Servlet Filter，再进入 Spring MVC 的 Interceptor，最后到达 Controller。

## 请求链路

```text
Client
  -> Filter
  -> DispatcherServlet
  -> Interceptor preHandle
  -> Controller
  -> Interceptor postHandle
  -> Interceptor afterCompletion
  -> Response
```

## Filter

Filter 属于 Servlet 体系，比 Spring MVC 更靠前，适合统一编码、跨域、粗粒度鉴权等。

```java
@Component
public class TraceFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        try {
            chain.doFilter(request, response);
        } finally {
            // 清理资源
        }
    }
}
```

## 登录验证过滤器

```java
public class LoginFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        String token = httpRequest.getHeader("Authorization");
        if (token == null) {
            httpResponse.setStatus(401);
            return;
        }

        chain.doFilter(request, response);
    }
}
```

## Interceptor

Interceptor 属于 Spring MVC，能拿到 Handler，更适合权限判断、登录态解析、日志耗时统计。

```java
public class LoggingInterceptor implements HandlerInterceptor {
    private static final ThreadLocal<Long> START_TIME = new ThreadLocal<>();

    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) {
        START_TIME.set(System.currentTimeMillis());
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler,
                                Exception ex) {
        long cost = System.currentTimeMillis() - START_TIME.get();
        START_TIME.remove();
        System.out.println(request.getRequestURI() + " cost " + cost + "ms");
    }
}
```

## WebMvcConfigurer

通过 `WebMvcConfigurer` 注册拦截器。

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    private final LoggingInterceptor loggingInterceptor;

    public WebConfig(LoggingInterceptor loggingInterceptor) {
        this.loggingInterceptor = loggingInterceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loggingInterceptor)
                .addPathPatterns("/**")
                .excludePathPatterns("/api/auth/login");
    }
}
```

## CORS 跨域设置

跨域可以用 Filter 实现，也可以用 MVC 配置实现。

```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOriginPatterns("*")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true);
    }
}
```

::: warning 注意
如果允许携带 Cookie 或认证信息，不要随意使用完全开放的跨域策略，生产环境应限制可信域名。
:::

