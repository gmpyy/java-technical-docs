---
title: Vue Composition API
description: 整理 script setup、ref、reactive、computed、watch、watchEffect、生命周期和 nextTick。
outline: [2, 3]
---

# Vue Composition API

Composition API 是现代 Vue3 项目的主线。它把状态、派生状态、副作用和生命周期放在同一个逻辑闭包里，更适合按业务功能组织代码，也更方便抽成 composables。

## script setup

现代 Vue3 项目建议使用 `<script setup>`：

```vue
<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)

const add = () => {
  count.value++
}
</script>

<template>
  <button @click="add">{{ count }}</button>
</template>
```

特点：

- 顶层变量可以直接在模板中使用。
- 不需要手动 `return`。
- 更适合 TypeScript 类型推导。
- 和 `defineProps`、`defineEmits`、`defineModel` 等编译宏配合使用。

## ref

`ref` 适合基本类型，也可以包对象：

```ts
const count = ref(0)
const name = ref('Vue')
```

在脚本中读写需要 `.value`：

```ts
count.value++
```

模板中会自动解包：

```vue
<p>{{ count }}</p>
```

`ref` 常用于：

- 数字、字符串、布尔值。
- DOM 引用。
- 弹窗开关。
- 当前页码、搜索关键词。

## reactive

`reactive` 适合对象：

```ts
const form = reactive({
  username: '',
  password: ''
})
```

注意：

- `reactive` 返回代理对象。
- 不要整体解构后直接使用，否则容易丢失响应式。
- 如果需要解构给模板用，可以用 `toRefs`。
- Pinia store 解构状态时优先使用 `storeToRefs`。

## computed

`computed` 用于从已有状态派生新状态：

```ts
const total = computed(() => price.value * count.value)
```

适用场景：

- 根据列表计算总数。
- 根据状态计算按钮是否禁用。
- 根据筛选条件得到展示数据。

`computed` 有缓存，依赖不变时不会重复计算。不要在 `computed` 中发送请求或修改外部状态。

## watch

`watch` 用于监听明确的数据源并执行副作用：

```ts
watch(keyword, async (value) => {
  await fetchList(value)
})
```

监听 getter：

```ts
watch(
  () => form.categoryId,
  () => {
    page.value = 1
    fetchList()
  },
  { immediate: true }
)
```

适用场景：

- 搜索条件变化后重新请求。
- 路由参数变化后刷新详情。
- 表单字段变化后联动其他字段。

## watchEffect

`watchEffect` 会自动收集同步执行过程中读取到的依赖：

```ts
watchEffect(() => {
  console.log(keyword.value, page.value)
})
```

适合依赖较多、且依赖关系清晰的副作用。需要精确控制监听源时，优先用 `watch`。

## watcher 清理

请求类副作用要考虑过期请求：

```ts
watch(keyword, async (value, _oldValue, onCleanup) => {
  const controller = new AbortController()
  onCleanup(() => controller.abort())

  await fetch(`/api/search?q=${value}`, {
    signal: controller.signal
  })
})
```

这样新一轮监听触发时，可以清理上一轮未完成任务，避免旧响应覆盖新状态。

## 生命周期

组合式 API 常用生命周期：

```ts
onMounted(() => {
  fetchList()
})

onUnmounted(() => {
  stopTimer()
})
```

常见对应关系：

| Options API | Composition API |
| --- | --- |
| `beforeCreate` / `created` | `setup` |
| `mounted` | `onMounted` |
| `updated` | `onUpdated` |
| `beforeUnmount` | `onBeforeUnmount` |
| `unmounted` | `onUnmounted` |

## nextTick

Vue 更新 DOM 是异步批处理的。修改数据后如果立刻读取 DOM，可能读到旧结果：

```ts
items.value.push(newItem)
await nextTick()
listRef.value?.scrollIntoView()
```

适用场景：

- 新增元素后滚动到底部。
- 弹窗打开后聚焦输入框。
- 状态变化后测量 DOM 尺寸。

## 使用边界

- 派生状态用 `computed`。
- 明确监听源用 `watch`。
- 自动依赖收集用 `watchEffect`。
- DOM 更新后读尺寸用 `nextTick`。
- 复用业务逻辑时抽成 composables。
