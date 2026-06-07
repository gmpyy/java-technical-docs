---
title: Vue 状态与请求
description: 整理 Pinia、状态持久化、Axios 封装、拦截器、API 模块和 mock 数据。
outline: [2, 3]
---

# Vue 状态与请求

现代 Vue 项目中，跨页面业务状态优先使用 Pinia，网络请求统一通过 Axios 实例和 API 模块封装。这样可以把 token、loading、错误处理、登录失效和接口路径集中管理。

## Pinia 安装与注册

Pinia 是现代 Vue 项目的默认状态管理方案。Vuex 仍然常见于 Vue2 或历史项目，新项目优先 Pinia。

```bash
pnpm add pinia
```

```ts
import { createPinia } from 'pinia'

app.use(createPinia())
```

## setup store

```ts
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const profile = ref<UserProfile | null>(null)

  const isLogin = computed(() => Boolean(token.value))

  const setToken = (value: string) => {
    token.value = value
  }

  const clearUser = () => {
    token.value = ''
    profile.value = null
  }

  return {
    token,
    profile,
    isLogin,
    setToken,
    clearUser
  }
})
```

组件中使用：

```ts
const userStore = useUserStore()
```

## storeToRefs

直接解构 store 会丢失响应式，状态建议使用 `storeToRefs`：

```ts
const userStore = useUserStore()
const { token, profile } = storeToRefs(userStore)
const { clearUser } = userStore
```

## 异步 action

```ts
export const useArticleStore = defineStore('article', () => {
  const list = ref<Article[]>([])

  const fetchList = async () => {
    const res = await getArticleListAPI()
    list.value = res.data
  }

  return {
    list,
    fetchList
  }
})
```

## 持久化

常见方式：

- 使用 `pinia-plugin-persistedstate`。
- 手动封装 `localStorage`。

手动封装示例：

```ts
export const setItem = (key: string, value: unknown) => {
  localStorage.setItem(key, JSON.stringify(value))
}

export const getItem = <T>(key: string): T | null => {
  return JSON.parse(localStorage.getItem(key) || 'null')
}

export const removeItem = (key: string) => {
  localStorage.removeItem(key)
}
```

退出登录时要清理 token、用户信息和相关持久化数据，避免下次进入页面时读到旧状态。

## Axios 请求实例

项目中通常通过 axios 拦截器统一处理 token、loading、错误提示和登录失效。

```ts
import axios from 'axios'

export const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000
})
```

## 请求拦截器

统一携带 token：

```ts
request.interceptors.request.use((config) => {
  const userStore = useUserStore()

  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }

  return config
})
```

如果接口要求特殊 header：

```ts
config.headers['Access-Token'] = token
config.headers.platform = 'H5'
```

## 响应拦截器

```ts
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      const userStore = useUserStore()
      userStore.clearUser()
      router.replace('/login')
    }

    return Promise.reject(error)
  }
)
```

注意：

- `Promise.reject` 后，调用方的 `await` 会进入异常流程。
- 业务错误提示可以在响应拦截器统一处理。
- loading 可以在请求开始和请求结束时统一控制。

## API 模块

不要在组件里散落 URL，建议封装 API 函数：

```ts
export const loginAPI = (data: LoginForm) => {
  return request.post<LoginResult>('/login', data)
}

export const getArticleListAPI = (params: ArticleQuery) => {
  return request.get<ArticleListResult>('/articles', { params })
}
```

组件中只调用 API：

```ts
const res = await loginAPI(form)
```

## mock 数据

没有后端时，可以用 `json-server` 或 mock 服务先完成页面逻辑。

常见流程：

1. 准备 `db.json`。
2. 启动 mock 服务。
3. 前端通过 axios 请求本地接口。
4. 后续替换真实后端时，主要修改 baseURL 和 API 层。

## 请求实践清单

- API 层统一管理接口。
- 请求拦截器统一加 token。
- 响应拦截器统一处理登录失效。
- loading 和错误提示可以统一封装。
- 组件只处理和当前页面相关的成功逻辑。
