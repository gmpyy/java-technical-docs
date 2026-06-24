---
title: "React Notes: Next Project"
description: "React.md source note section: Next Project."
outline: [2, 3]
---

# next项目开发

路由：app\-router

组件：默认是server component，还有client component（需要在文件最上面添加useclient）

嵌套逻辑：一般都是server component里面去定义client component，如果client component里面有server component，它会自动变成client component

Server component：里面定义一些常量，最终返回的是html，所以只能写好一些静态的东西

Client component：可以使用一些hooks，比如说usestate

Nextjs route handler





构建工具：turbopack





通过ref和useeffect实现只要聊天消息有变化，都会回到底部



修复高危漏洞：

![Image](/images/react-notes/image-08.png)





空心圆表示静态内容，f表示动态，静态内容会缓存，如果里面有像发请求的，就会缓存第一次请求的结果，后续不再重新请求。

![Image](/images/react-notes/image-09.png)





什么是ssg：

纯静态页面，比如说技术文档这些没有交互的东西，就可以使用ssg





mdx：markdown里面可以嵌套react组件





页面需要拆分成多个组件时的目录结构：

page\.tsx 只是这个路由的入口组件，不需要把所有 tsx 都堆进去。更常见的做法是让 page\.tsx 只负责“组装页面”，把大块内容拆到普通组件里，也就是\_component目录下面的文件：

```Java
src/
└── app/
    └── xiaoman/
        ├── page.tsx
        ├── _components/
        │   ├── Hero.tsx
        │   ├── ArticleList.tsx
        │   └── Footer.tsx
        └── _lib/
            └── data.ts

```

几个建议：

- 只在路由入口放 page\.tsx，其余页面块拆成普通组件。

- 某个页面专用的组件，就放在这个路由目录下，比如 app/xiaoman/\_components。

- 多个页面都会复用的组件，再提到 src/components。

- 如果某个拆出去的组件用了 useState、useEffect、点击事件这些客户端能力，就只在那个组件文件顶部加 'use client'，不要一上来把整个 page\.tsx 都变成客户端组件。

- 官方也明确说明了：app 里可以安全地 colocate 项目文件；而 \_folder 这种私有文件夹会被排除出路由系统，特别适合放 \_components、\_lib 这类内部实现文件。

正常的项目结构：

```Java
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── xiaoman/
│   │   ├── page.tsx
│   │   ├── loading.tsx
│   │   ├── error.tsx
│   │   ├── _components/
│   │   │   ├── Hero.tsx
│   │   │   ├── ArticleList.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── _lib/
│   │   │   ├── data.ts
│   │   │   └── format.ts
│   │   └── _types/
│   │       └── index.ts
│   └── daman/
│       ├── page.tsx
│       ├── _components/
│       │   └── Hero.tsx
│       └── _lib/
│           └── data.ts
├── components/
│   └── ui/
│       ├── Button.tsx
│       └── Card.tsx
├── lib/
│   ├── request.ts
│   └── utils.ts
└── types/
    └── global.ts
```

但是组件也可以直接放在页面目录下面，只要他不是特殊文件名，比如page\.tsx、layout\.tsx、template\.tsx、loading\.tsx、error\.tsx、not\-found\.tsx、route\.ts就完全可以。

```Java
src/
└── app/
    └── xiaoman/
        ├── page.tsx
        ├── Hero.tsx
        ├── ArticleList.tsx
        └── _lib/
            └── data.ts
```

更常用的项目结构：

```Java
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   ├── (marketing)/
│   │   ├── page.tsx
│   │   ├── about/
│   │   │   └── page.tsx
│   │   └── contact/
│   │       └── page.tsx
│   ├── (main)/
│   │   ├── xiaoman/
│   │   │   ├── page.tsx
│   │   │   ├── loading.tsx
│   │   │   ├── error.tsx
│   │   │   └── not-found.tsx
│   │   └── daman/
│   │       └── page.tsx
│   └── api/
│       └── articles/
│           └── route.ts
├── features/
│   ├── xiaoman/
│   │   ├── components/
│   │   │   ├── Hero.tsx
│   │   │   ├── ArticleList.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── services/
│   │   │   └── getXiaomanData.ts
│   │   ├── hooks/
│   │   │   └── useXiaomanFilter.ts
│   │   ├── types.ts
│   │   └── utils.ts
│   └── daman/
│       ├── components/
│       ├── services/
│       └── types.ts
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Modal.tsx
│   └── shared/
│       ├── Header.tsx
│       └── Footer.tsx
├── lib/
│   ├── request.ts
│   ├── auth.ts
│   ├── db.ts
│   └── utils.ts
├── hooks/
│   └── useDebounce.ts
├── store/
│   └── userStore.ts
├── constants/
│   └── index.ts
└── types/
    └── global.d.ts
```

- app：只放路由相关文件，像 page\.tsx、layout\.tsx、loading\.tsx、error\.tsx、route\.ts

- features：按业务模块拆分，比如“小满模块”“大满模块”

- components/ui：通用 UI 组件，任何页面都能复用

- components/shared：站点级公共组件，比如头部、底部

- lib：跨业务的工具、请求、鉴权、数据库

- hooks/store/types/constants：全局能力
