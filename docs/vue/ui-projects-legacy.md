---
title: Vue UI、项目实践与旧项目维护
description: 整理 Element Plus、Vant、智慧商城、文章管理系统、Vue2、Vuex、event bus 和 mixins。
outline: [2, 3]
---

# Vue UI、项目实践与旧项目维护

这一章把组件库、真实项目案例和旧项目维护放在一起。PC 后台常见 Element Plus，移动端常见 Vant；旧项目中会遇到 Vue2、Vue CLI、Vuex、`.sync`、event bus 和 mixins。

## Element Plus

PC 后台常用 Element Plus：

```bash
pnpm add element-plus
```

常见组件：

- Form 表单校验。
- Container 布局。
- Menu 菜单。
- Table 表格。
- Pagination 分页。
- Dialog 弹窗。
- Drawer 抽屉。
- Upload 上传。
- MessageBox 确认框。
- Dropdown 下拉菜单。

自动导入常用组合：

- `unplugin-vue-components`
- `unplugin-auto-import`
- `ElementPlusResolver`

作用：

- 自动导入 Element Plus 组件。
- 自动导入 Vue API。
- 减少重复 import。

## Element Plus 表单校验

关键点：

- `model` 绑定表单对象。
- `rules` 绑定规则。
- `prop` 对应字段名。
- `ref` 调用校验方法。

```vue
<script setup lang="ts">
const formRef = ref<FormInstance>()

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const submit = async () => {
  await formRef.value?.validate()
  await loginAPI(form)
}
</script>

<template>
  <el-form ref="formRef" :model="form" :rules="rules">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="form.username" />
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input v-model="form.password" type="password" />
    </el-form-item>
  </el-form>
</template>
```

## 表格、筛选与分页

文章管理系统的列表页通常由三部分组成：

- 筛选表单。
- 数据表格。
- 分页器。

请求参数：

```ts
const query = reactive({
  page: 1,
  pageSize: 10,
  categoryId: '',
  state: ''
})
```

筛选时重置页码：

```ts
const onSearch = () => {
  query.page = 1
  fetchList()
}
```

分页变化：

```ts
const onCurrentChange = (page: number) => {
  query.page = page
  fetchList()
}
```

## Dialog、Drawer 与 Upload

简单新增编辑可以用 Dialog：

```vue
<el-dialog v-model="visible" title="编辑分类">
  <CategoryForm />
</el-dialog>
```

较复杂的文章编辑适合 Drawer：

```vue
<el-drawer v-model="drawerVisible" direction="rtl" size="50%">
  <ArticleForm />
</el-drawer>
```

Drawer 的好处是用户不离开列表页，提交或取消后能回到原来的筛选和分页上下文。

Element Plus 上传组件：

```vue
<el-upload :auto-upload="false" :on-change="onUploadFile">
  <el-button>上传</el-button>
</el-upload>
```

本地预览：

```ts
const imageUrl = ref('')

const onUploadFile = (uploadFile: UploadFile) => {
  if (uploadFile.raw) {
    imageUrl.value = URL.createObjectURL(uploadFile.raw)
  }
}
```

## Vant 与移动端适配

移动端智慧商城项目使用 Vant。Vue2 项目常见安装方式：

```bash
npm i vant@latest-v2 -S --legacy-peer-deps
npm i babel-plugin-import -D --legacy-peer-deps
```

建议把组件库注册抽离到：

```txt
src/plugins/vant.js
```

然后在入口文件中引入：

```js
import '@/plugins/vant'
```

移动端项目可以使用 `postcss-px-to-viewport`：

```bash
npm install postcss-px-to-viewport --save-dev
```

配置示例：

```js
module.exports = {
  plugins: {
    'postcss-px-to-viewport': {
      viewportWidth: 375
    }
  }
}
```

## Sass 变量自动注入

Vite 中可以配置全局 Sass 变量：

```ts
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/styles/variables.scss" as *;`
      }
    }
  }
})
```

适合放主题色、间距变量、mixin 和断点变量。

## 移动端智慧商城项目

技术点：

- Vue2
- Vant
- Vue Router
- Vuex
- Axios
- postcss-px-to-viewport

核心页面：

```txt
views/
  login/
  layout/
    home/
    category/
    cart/
    mydata/
  prodetail/
  search/
```

登录要点：

- 验证码接口返回 base64 时，可以直接作为图片地址。
- 手机号用正则校验。
- 登录成功后保存 token 和用户信息。
- 未登录访问购物车、个人中心时跳转登录。
- 登录成功后按 redirect 回跳。

```js
if (!/^1[3-9]\d{9}$/.test(mobile)) {
  Toast('手机号格式错误')
}
```

购物车要点：

- 商品详情页加入购物车。
- Vuex 管理购物车数量和商品列表。
- 修改数量要通过 mutation/action。
- 底部 tab 可以展示购物车角标。

## PC 文章管理系统

技术点：

- Vue3
- Vite
- Element Plus
- Pinia
- Vue Router
- Axios
- pnpm

核心模块：

- 登录 / 注册。
- 首页布局。
- 用户信息。
- 文章分类。
- 文章列表。
- 新增 / 编辑文章。
- 图片上传。

登录注册：

- 使用 Element Plus Form。
- 用户名、密码、确认密码做规则校验。
- 提交前调用 `formRef.validate()`。
- 登录成功后保存 token。
- 通过路由守卫保护后台页面。

退出登录：

```ts
await ElMessageBox.confirm('你确认要退出吗？', '温馨提示')
userStore.clearUser()
router.replace('/login')
```

文章编辑：

- 新增和编辑可以复用同一个表单。
- 编辑时先请求详情并回显。
- 图片上传后预览。
- 提交时根据是否有 id 判断新增或编辑。

## Vue2 与 Vue CLI

Vue CLI 基于 webpack，常见于旧项目。新项目推荐 Vite + `create-vue`。

旧项目仍需要掌握：

- `new Vue({ el, data, methods })`
- Options API
- Vue Router 3
- Vuex
- `this.$refs`
- `this.$router`
- `this.$store`

Vue2 示例：

```js
new Vue({
  el: '#app',
  data() {
    return {
      message: 'hello Vue'
    }
  }
})
```

## Vuex

Vuex 是 Vue2 项目中常见的集中状态管理方案，新项目优先 Pinia。

Vuex 核心概念：

- `state`：状态。
- `mutations`：同步修改状态。
- `actions`：异步逻辑。
- `getters`：派生状态。
- `modules`：分模块。

```js
const store = new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
    increment(state) {
      state.count++
    }
  }
})
```

迁移建议：

- `state` 迁移为 Pinia 中的 `ref` 或 `reactive`。
- `getters` 迁移为 `computed`。
- `mutations` 和 `actions` 合并为 store 中的方法。
- `mapState` 等辅助函数替换为 `storeToRefs`。

## 旧写法迁移

Vue2 中 `.sync` 用于父子双向同步：

```vue
<Child :title.sync="title" />
```

现代写法：

- Vue3.4+：`defineModel`。
- Vue3.0+：`modelValue` + `update:modelValue`。

Vue2 中常见 event bus：

```js
const bus = new Vue()
bus.$emit('change')
bus.$on('change', handler)
```

现代项目不推荐 event bus 作为主方案，优先选择 Pinia、props/emits、provide/inject 或 composables。

mixins 可以复用 Options API 逻辑，但容易带来命名冲突和来源不清晰。现代项目优先 composables。
