---
title: Vue 核心基础
description: 整理 Vue 模板语法、条件渲染、列表渲染、表单绑定和动态样式。
outline: [2, 3]
---

# Vue 核心基础

Vue 的模板语法把 HTML、响应式状态和声明式渲染组合在一起。基础语法不复杂，但真实项目里的可维护性往往取决于 key、表单绑定、条件渲染和样式绑定这些细节。

## 模板语法

插值表达式用于渲染文本：

```vue
<template>
  <p>{{ message }}</p>
</template>
```

动态属性使用 `v-bind`，简写为 `:`：

```vue
<img :src="imageUrl" :alt="title" />
```

事件绑定使用 `v-on`，简写为 `@`：

```vue
<button @click="submit">提交</button>
```

带参数事件：

```vue
<button @click="remove(item.id)">删除</button>
```

如果既需要原始事件参数，又要传业务参数：

```vue
<Child @input="handleInput($event, item.id)" />
```

## 条件渲染

```vue
<p v-if="isLogin">已登录</p>
<p v-else>未登录</p>
```

`v-if` 和 `v-show` 的区别：

| 指令 | 实现方式 | 适合场景 |
| --- | --- | --- |
| `v-if` | 控制 DOM 是否创建 | 条件不常变化 |
| `v-show` | 控制 CSS `display` | 高频切换 |

```vue
<section v-show="panelVisible">
  面板内容会保留 DOM，只切换显示状态
</section>
```

## 列表渲染

```vue
<ul>
  <li v-for="item in list" :key="item.id">
    {{ item.name }}
  </li>
</ul>
```

要点：

- `key` 应该使用稳定唯一值。
- 不建议在复杂列表中使用数组下标作为 `key`。
- 列表项有增删改排序时，稳定 `key` 能减少错误复用。

列表项中可以继续绑定事件：

```vue
<article v-for="article in articles" :key="article.id">
  <h3>{{ article.title }}</h3>
  <button @click="editArticle(article.id)">编辑</button>
</article>
```

## 表单绑定

```vue
<input v-model="form.username" />
```

常用修饰符：

```vue
<input v-model.trim="name" />
<input v-model.number="age" />
<input v-model.lazy="keyword" />
```

含义：

- `.trim`：去掉首尾空格。
- `.number`：尽量转成数字。
- `.lazy`：在 change 时同步，而不是 input 时同步。

多字段表单常见写法：

```vue
<script setup lang="ts">
import { reactive } from 'vue'

const form = reactive({
  username: '',
  password: '',
  remember: false
})
</script>

<template>
  <input v-model.trim="form.username" />
  <input v-model="form.password" type="password" />
  <input v-model="form.remember" type="checkbox" />
</template>
```

## class 与 style

对象语法：

```vue
<div :class="{ active: isActive, disabled: disabled }"></div>
```

数组语法：

```vue
<div :class="['card', currentKind, { selected }]"></div>
```

动态 style：

```vue
<div :style="{ color: textColor, fontSize: size + 'px' }"></div>
```

项目中建议把主要样式放到 CSS 或预处理器里，模板中只绑定状态类名。

## 图片资源

静态导入：

```ts
import logo from '@/assets/logo.png'
```

模板使用：

```vue
<img :src="logo" alt="logo" />
```

public 资源可以直接用绝对路径：

```vue
<img src="/logo.png" alt="logo" />
```

## 基础检查表

- 条件频繁切换优先 `v-show`，否则用 `v-if`。
- 列表必须有稳定 `key`。
- 表单输入需要结合 `.trim`、`.number` 等修饰符处理数据。
- 事件处理函数不要在模板里堆太多复杂表达式。
- 动态样式优先绑定 class，少量动态值再使用 style。
