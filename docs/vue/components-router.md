---
title: Vue 组件与路由
description: 整理 Vue 组件通信、defineModel、slots、composables 和 Vue Router 4。
outline: [2, 3]
---

# Vue 组件与路由

组件负责拆分界面和封装交互，路由负责组织页面。现代 Vue 项目中，组件通信以 props、emits、`defineModel`、slots、provide/inject 和 Pinia 为主；路由以 Vue Router 4 和组合式 API 为主。

## props

父组件传值：

```vue
<UserCard :user="user" />
```

子组件接收：

```vue
<script setup lang="ts">
interface User {
  id: number
  name: string
}

defineProps<{
  user: User
}>()
</script>
```

props 是只读输入，子组件不要直接修改父组件传入的数据。

## emit

子组件通知父组件：

```vue
<script setup lang="ts">
const emit = defineEmits<{
  save: [id: number]
}>()

const handleSave = () => {
  emit('save', 1)
}
</script>
```

父组件监听：

```vue
<UserCard @save="handleSave" />
```

## defineModel

Vue 3.4+ 推荐用 `defineModel` 封装组件双向绑定：

```vue
<script setup lang="ts">
const model = defineModel<string>()
</script>

<template>
  <input v-model="model" />
</template>
```

父组件使用：

```vue
<BaseInput v-model="username" />
```

如果需要兼容旧版本 Vue3，可以使用 `modelValue` + `update:modelValue`：

```vue
<script setup lang="ts">
defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <input
    :value="modelValue"
    @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
  />
</template>
```

## template ref 与 defineExpose

获取 DOM：

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const inputRef = ref<HTMLInputElement | null>(null)

onMounted(() => {
  inputRef.value?.focus()
})
</script>

<template>
  <input ref="inputRef" />
</template>
```

子组件默认不会把所有内部状态暴露给父组件。需要父组件通过 ref 调用时，用 `defineExpose`：

```vue
<script setup lang="ts">
const reset = () => {}

defineExpose({
  reset
})
</script>
```

## provide / inject

适合跨层级传递稳定依赖：

```ts
provide('theme', theme)
```

```ts
const theme = inject('theme')
```

适用场景：

- 主题配置。
- 表单上下文。
- 布局上下文。
- 当前模块级状态。

如果是全局业务状态，优先使用 Pinia。

## slots

默认插槽：

```vue
<BaseCard>
  <p>内容</p>
</BaseCard>
```

子组件：

```vue
<template>
  <section>
    <slot />
  </section>
</template>
```

具名插槽：

```vue
<template #footer>
  <button>确定</button>
</template>
```

作用域插槽：

```vue
<template #default="{ row }">
  {{ row.title }}
</template>
```

## composables

现代 Vue 推荐用 composables 复用逻辑：

```ts
export function usePagination(fetcher: () => Promise<void>) {
  const page = ref(1)
  const pageSize = ref(10)
  const total = ref(0)

  const reset = async () => {
    page.value = 1
    await fetcher()
  }

  return {
    page,
    pageSize,
    total,
    reset
  }
}
```

适合抽离：

- 分页逻辑。
- 搜索筛选逻辑。
- 弹窗打开关闭逻辑。
- 权限判断。
- 上传预览。
- 滚动监听。

## Vue Router 4 基础配置

```ts
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      component: () => import('@/views/home/index.vue')
    },
    {
      path: '/login',
      component: () => import('@/views/login/index.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      component: () => import('@/views/not-found/index.vue')
    }
  ]
})

export default router
```

在 `main.ts` 中注册：

```ts
app.use(router)
```

## 路由出口与跳转

路由出口：

```vue
<router-view />
```

声明式导航：

```vue
<router-link to="/home">首页</router-link>
```

编程式导航：

```ts
const router = useRouter()

router.push('/home')
```

读取路由信息：

```ts
const route = useRoute()
const id = route.params.id
```

## 嵌套路由

后台布局常用嵌套路由：

```ts
{
  path: '/',
  component: () => import('@/views/layout/index.vue'),
  redirect: '/article',
  children: [
    {
      path: 'article',
      component: () => import('@/views/article/index.vue')
    },
    {
      path: 'category',
      component: () => import('@/views/category/index.vue')
    }
  ]
}
```

父页面中放二级路由出口：

```vue
<router-view />
```

## 路由守卫

登录拦截：

```ts
router.beforeEach((to) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.token) {
    return {
      path: '/login',
      query: {
        redirect: to.fullPath
      }
    }
  }
})
```

登录成功后回跳：

```ts
const redirect = route.query.redirect?.toString() || '/'
router.replace(redirect)
```

## keep-alive

需要缓存列表页时使用：

```vue
<router-view v-slot="{ Component }">
  <keep-alive include="ArticleList">
    <component :is="Component" />
  </keep-alive>
</router-view>
```

适合场景：

- 从详情返回列表时保留筛选和滚动位置。
- 多 tab 页面切换时保留内部状态。
