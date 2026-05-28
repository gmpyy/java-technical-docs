# Java 技术文档

这是基于 `D:\Users\gmpyy\Downloads\JAVA.md` 重新整理的 Markdown + VitePress 文档站。

## 本地运行

当前机器需要先安装 npm、pnpm 或 yarn 之一。安装好包管理器后执行：

```bash
npm install
npm run docs:dev
```

构建静态站点：

```bash
npm run docs:build
```

构建产物位于：

```text
docs/.vitepress/dist
```

## 内容结构

- `docs/index.md`：文档首页和学习路线。
- `docs/java/`：Java 基础、语法、集合、面向对象、数据库基础。
- `docs/springboot/`：Spring Boot 分层、请求参数、依赖注入、Web 链路、认证、事务和定时任务。
- `docs/middleware/`：RabbitMQ。
- `docs/redis/`：Redis 基础、缓存锁、Stream、GEO、Bitmap、HyperLogLog。
- `docs/public/images/source/`：从原 `JAVA.md` 内部图片链接本地化保存的图片归档。

## 说明

旧版自定义 HTML/JSON/脚本生成方案已经移除。当前内容源就是 Markdown 文件，网站渲染交给 VitePress 默认主题。
