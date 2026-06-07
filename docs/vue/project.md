---
title: Vue 项目主线
description: 整理 Vue3、Vite、create-vue、TypeScript、项目目录和工程化入口。
outline: [2, 3]
---

# Vue 项目主线

现代 Vue 新项目建议以 Vue3、Vite、TypeScript、`<script setup>`、Vue Router 4、Pinia 和 Axios 作为默认主线。Vue CLI 和 Vuex 仍然常见于旧项目，但新项目优先使用 Vite 与 Pinia。

## 推荐技术栈

新项目可以默认选择：

- Vue3
- Vite
- TypeScript
- `<script setup>`
- Vue Router 4
- Pinia
- Axios
- Element Plus 或 Vant
- ESLint / Prettier
- Vitest / Playwright

官方创建方式：

```bash
npm create vue@latest
```

或：

```bash
pnpm create vue@latest
```

这里使用的是官方脚手架 `create-vue`，底层开发体验以 Vite 为主。

## 创建项目时的选择

创建时可以按项目需要选择：

- TypeScript
- Vue Router
- Pinia
- Vitest
- E2E 测试
- ESLint
- Prettier

启动开发：

```bash
pnpm install
pnpm run dev
```

生产构建：

```bash
pnpm run build
```

## 推荐目录结构

中大型后台或移动端项目可以按下面组织：

```txt
src/
  api/
    user.ts
    article.ts
  assets/
  components/
  composables/
    useAuth.ts
    usePagination.ts
  router/
    index.ts
  stores/
    user.ts
    article.ts
  types/
    user.ts
    article.ts
  utils/
    request.ts
    storage.ts
  views/
  App.vue
  main.ts
```

## 目录职责

| 目录 | 职责 |
| --- | --- |
| `api/` | 接口函数，只负责请求，不写页面逻辑 |
| `stores/` | 全局状态，例如用户信息、token、购物车 |
| `composables/` | 可复用组合逻辑，例如分页、权限、表单 |
| `router/` | 路由表、路由守卫和页面跳转规则 |
| `utils/` | 请求实例、本地存储、格式化工具 |
| `types/` | 接口数据类型和业务类型 |
| `views/` | 页面级组件 |
| `components/` | 可复用 UI 组件 |

## 入口文件

入口文件负责创建 Vue 应用并挂载插件：

```ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.mount('#app')
```

入口文件应该保持清爽。组件库注册、请求实例、全局样式、状态管理和路由配置都可以拆到单独模块。

## 工程化原则

### 页面只编排，不堆工具逻辑

页面组件负责组织数据、调用 API、组合业务组件。复杂分页、上传、权限判断等逻辑可以抽到 composables 或 store。

```ts
const { page, pageSize, total, reset } = usePagination(fetchList)
```

### API 层统一管理接口

不要在组件里散落 URL：

```ts
export const getArticleListAPI = (params: ArticleQuery) => {
  return request.get<ArticleListResult>('/articles', { params })
}
```

组件只关心业务动作：

```ts
const res = await getArticleListAPI(query)
```

### 状态按生命周期选择位置

- 只在当前组件使用：放组件内。
- 多个兄弟组件共享：提升到共同父组件或 composable。
- 跨页面共享：放 Pinia。
- 服务端列表数据：优先接口请求，不要全部塞进全局 store。
