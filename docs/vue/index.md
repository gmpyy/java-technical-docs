---
title: Vue 技术文档
description: 以 Vue3、Vite、Composition API、Vue Router、Pinia 和项目实践为主线的 Vue 技术文档。
outline: [2, 3]
---

# Vue 技术文档

这套文档把 Vue 知识整理成面向项目落地的技术资料。主线采用 Vue3、Vite、`<script setup>`、Vue Router 4、Pinia 和 Axios；Vue2、Vue CLI、Vuex、`.sync`、event bus、mixins 等内容作为旧项目维护与迁移知识单独归档。

Vue 的核心思想可以概括为：用模板描述界面，用响应式数据驱动更新，用组件拆分复杂 UI，用路由组织页面，用状态管理承载跨页面业务状态。

```vue
<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <button @click="count++">当前计数：{{ count }}</button>
</template>
```

## 阅读路线

1. 先看项目主线，理解 Vue3 + Vite 项目怎么创建、目录怎么分层。
2. 再看 Vue 核心基础，掌握模板、条件、列表、表单和动态样式。
3. 接着看 Composition API，把 `ref`、`reactive`、`computed`、`watch`、生命周期串起来。
4. 然后看组件、路由、Pinia 和 Axios，把单页面应用的数据流打通。
5. 最后看组件库、项目实践和旧项目迁移，补齐真实项目里的常见场景。

## 章节地图

| 章节 | 内容范围 |
| --- | --- |
| [项目主线](/vue/project) | Vue3、Vite、`create-vue`、TypeScript、目录结构、工程化入口 |
| [核心基础](/vue/basics) | 模板语法、条件渲染、列表渲染、表单绑定、class/style |
| [Composition API](/vue/composition) | `<script setup>`、`ref`、`reactive`、`computed`、`watch`、生命周期、`nextTick` |
| [组件与路由](/vue/components-router) | props、emits、`defineModel`、slots、composables、Vue Router 4 |
| [状态与请求](/vue/state-request) | Pinia、持久化、Axios、请求拦截器、响应拦截器、API 模块、mock |
| [UI、项目与旧项目维护](/vue/ui-projects-legacy) | Element Plus、Vant、智慧商城、文章管理系统、Vue2、Vuex、event bus、mixins |

## 知识覆盖表

| 原始主题 | 文档位置 |
| --- | --- |
| Vue3 项目创建 | [项目主线](/vue/project) |
| Vue 基础指令 | [核心基础](/vue/basics) |
| Composition API | [Composition API](/vue/composition) |
| 组件通信 | [组件与路由](/vue/components-router) |
| Vue Router | [组件与路由](/vue/components-router) |
| Pinia / Vuex | [状态与请求](/vue/state-request)、[UI、项目与旧项目维护](/vue/ui-projects-legacy) |
| Axios 封装 | [状态与请求](/vue/state-request) |
| 智慧商城 | [UI、项目与旧项目维护](/vue/ui-projects-legacy) |
| 文章管理系统 | [UI、项目与旧项目维护](/vue/ui-projects-legacy) |

## 核心心智模型

### 数据驱动视图

Vue 中不要把 DOM 当成主要操作对象。多数界面变化都应该通过修改响应式状态完成，Vue 再根据状态重新计算模板并更新真实 DOM。

```vue
<script setup>
import { ref } from 'vue'

const visible = ref(true)
</script>

<template>
  <button @click="visible = !visible">切换</button>
  <p v-if="visible">这段内容由状态控制</p>
</template>
```

### 组件负责边界

页面越复杂，越需要把 UI 拆成页面组件、业务组件和基础组件。组件通过 props、emits、slots、`defineModel` 和 Pinia 交换数据，而不是互相直接改内部状态。

### 工程化负责长期维护

真实项目不只是写组件，还包括路由分层、接口封装、token 管理、状态持久化、表单校验、上传预览、打包部署和旧项目迁移。后面的章节会按这些场景展开。
