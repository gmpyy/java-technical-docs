---
title: React 基础模型
description: 整理 React 概念与特性、Real DOM 与 Virtual DOM、JSX 编译和从组件到真实 DOM 的过程。
outline: [2, 3]
---

# React 基础模型

React 是用于构建用户界面的 JavaScript 库。它最核心的能力不是某个单独 API，而是一整套 UI 组织模型：用组件拆分界面，用 props 和 state 描述数据，用 React Element 表示 UI 结果，再通过调和过程把变化提交到真实宿主环境。

## React 概念与特性

React 概念与特性可以从五个方向理解：

| 特性 | 作用 |
| --- | --- |
| 声明式 UI | 开发者描述当前状态下界面应该是什么样，React 负责把差异更新到界面 |
| 组件化 | 把页面拆成可组合、可复用、可测试的单元 |
| 单向数据流 | 数据从父到子流动，子组件通过回调表达动作 |
| 虚拟 DOM | 用普通对象描述 UI，作为调和算法的输入 |
| 跨平台模型 | 同一套组件思想可以对应 DOM、Native、服务端字符串或其他宿主环境 |

```tsx
type ProductCardProps = {
  title: string
  price: number
  selected: boolean
  onSelect: () => void
}

export function ProductCard(props: ProductCardProps) {
  return (
    <article data-selected={props.selected}>
      <h2>{props.title}</h2>
      <strong>¥{props.price}</strong>
      <button onClick={props.onSelect}>选择</button>
    </article>
  )
}
```

这段代码没有直接创建 DOM，也没有描述“先创建哪个节点、再设置哪个属性”。组件只是根据输入返回界面描述。React 在后续流程中负责把描述转换成实际更新。

### React 适合解决的问题

React 适合需要频繁响应状态变化的界面，例如后台管理系统、复杂表单、数据看板、协作工具、移动端 Web、跨端应用和需要局部高频交互的页面。它把 UI 变化收束到状态变化上，让开发者少写直接 DOM 操作。

React 不是完整框架。路由、请求、状态管理、样式方案、服务端渲染、测试策略都需要根据项目选择生态工具。这个特点带来自由度，也要求团队建立工程约定。

## Real DOM 与 Virtual DOM

Real DOM 是浏览器真实维护的节点树。直接操作 Real DOM 可以完成任何界面更新，但在复杂应用中，手动维护节点、属性、事件、状态同步和卸载清理成本很高。

Virtual DOM 是对 UI 的 JavaScript 对象描述。它不是浏览器对象，也不是让单次 DOM 操作天然更快的魔法。它的价值在于把“状态到界面”的更新过程标准化：每次状态变化后重新得到一棵描述树，React 比较新旧描述，计算需要提交的最小变化。

```tsx
const element = (
  <button className="primary" disabled={false}>
    保存
  </button>
)
```

可以把这个 JSX 结果理解成类似下面的对象：

```ts
const element = {
  type: 'button',
  key: null,
  ref: null,
  props: {
    className: 'primary',
    disabled: false,
    children: '保存'
  }
}
```

真实 React Element 还有内部标记，但心智模型就是：React 先拿到不可变描述，再根据描述建立或更新 Fiber 节点。

### 两者的优缺点

| 维度 | Real DOM | Virtual DOM |
| --- | --- | --- |
| 操作方式 | 直接命令式修改节点 | 通过状态得到 UI 描述 |
| 单次小改动 | 手写可能更直接 | 需要一次描述与调和流程 |
| 复杂状态同步 | 容易散落在各处 | 状态更新入口更统一 |
| 跨平台 | 依赖浏览器 DOM | 可以映射到不同宿主环境 |
| 可维护性 | 大型应用中手工成本高 | 组件模型更稳定 |

Virtual DOM 的主要代价是运行时计算和内存对象创建。React 通过 key、diff 假设、Fiber 调度、批处理、memo 和编译工具不断降低成本。实际项目中，性能瓶颈往往不是“用了虚拟 DOM”，而是状态放置不合理、渲染范围过大、列表过长或重复计算过多。

## React Element、Component 与 Instance

React 开发中经常混淆 Component、Element 和 Instance。

| 名称 | 含义 | 说明 |
| --- | --- | --- |
| Component | 组件定义 | 函数组件或类组件本身 |
| React Element | 组件执行或 JSX 表达式的结果 | 普通不可变描述对象 |
| Instance | 类组件运行时实例 | 函数组件没有传统实例 |

```tsx
function UserName({ name }: { name: string }) {
  return <span>{name}</span>
}

const element = <UserName name="Lin" />
```

这里 `UserName` 是组件定义，`element` 是 React Element。React 根据 Element 的 `type` 判断这是原生标签还是自定义组件，再进入下一步处理。

类组件才有传统实例：

```tsx
class UserNameClass extends React.Component<{ name: string }> {
  render() {
    return <span>{this.props.name}</span>
  }
}
```

类组件实例保存 `this.props`、`this.state` 和实例方法。函数组件则依靠 Hook 保存状态单元，不暴露类实例。

## JSX 转换为真实 DOM

JSX 转换为真实 DOM可以拆成四个阶段：

1. 构建阶段把 JSX 编译成创建 React Element 的函数调用。
2. 运行时执行组件，得到新的 React Element 树。
3. React 根据 Element 树构建或更新 Fiber 树，完成调和。
4. 提交阶段把需要插入、更新、删除的内容应用到真实 DOM。

旧 JSX runtime 会把 JSX 编译为 `React.createElement`：

```tsx
const view = <h1 className="title">Hello React</h1>
```

等价思想如下：

```ts
const view = React.createElement(
  'h1',
  { className: 'title' },
  'Hello React'
)
```

新 JSX runtime 会自动从 `react/jsx-runtime` 引入创建函数，所以很多现代项目不再要求每个 JSX 文件都显式 `import React from 'react'`。但本质仍然是创建 React Element。

### 从 Element 到 DOM

一个简单组件的更新路径如下：

```tsx
function StatusLabel({ status }: {
  status: 'idle' | 'loading' | 'done'
}) {
  return (
    <span data-status={status}>
      {status === 'loading' ? '加载中' : '完成'}
    </span>
  )
}
```

当 `status` 从 `loading` 变成 `done` 时，React 会重新执行组件，得到新的 Element。类型仍然是 `span`，所以真实 DOM 节点可以复用；变化集中在 `data-status` 属性和文本内容上。

## JSX 的价值与限制

JSX 把 UI 结构和对应逻辑放在同一个 JavaScript 表达式里。它既不是字符串模板，也不是浏览器语法，而是构建工具可以转换的语法扩展。

```tsx
function EmptyState({ count }: { count: number }) {
  return (
    <section>
      {count === 0 ? (
        <p>暂无数据</p>
      ) : (
        <p>共 {count} 条记录</p>
      )}
    </section>
  )
}
```

JSX 花括号里写的是 JavaScript 表达式，而不是任意语句。复杂逻辑应提前计算，避免 render 中混入大量流程控制。

```tsx
function UserBadge({ user }: {
  user?: { name: string; locked: boolean }
}) {
  if (!user) {
    return <span>未登录</span>
  }

  const label = user.locked ? `${user.name}（已锁定）` : user.name
  return <strong>{label}</strong>
}
```

这类写法比在 JSX 内塞入多层三元表达式更容易维护。

## React 更新的基本路径

React 更新并不是“直接修改变量后界面自动变”。更新需要进入 React 的状态入口。

```tsx
function SaveButton() {
  const [saved, setSaved] = React.useState(false)

  return (
    <button onClick={() => setSaved(true)}>
      {saved ? '已保存' : '保存'}
    </button>
  )
}
```

点击按钮后发生的是：

1. 事件处理函数调用 `setSaved(true)`。
2. React 记录一次状态更新。
3. React 安排对应组件重新渲染。
4. 组件函数再次执行，得到新的 Element。
5. 调和阶段比较新旧结果。
6. 提交阶段更新按钮文本。

理解这条路径有助于判断很多问题：为什么直接改对象不会刷新，为什么旧闭包会读到旧值，为什么 props 改变会触发子组件执行，为什么 key 会影响列表状态复用。

## 基础模型检查清单

| 检查项 | 建议 |
| --- | --- |
| UI 表达 | 组件返回的是当前状态下的界面描述 |
| 数据变化 | 通过 state setter、`setState`、store 或路由状态进入 React 更新流程 |
| DOM 操作 | 优先状态驱动，只有聚焦、测量、滚动、第三方库等场景使用 ref |
| JSX | 理解它会变成 Element 创建调用 |
| Virtual DOM | 关注可维护性和调和模型，不把它误解为所有场景的性能保证 |
| 组件边界 | 每个组件尽量围绕明确的输入、输出和副作用边界组织 |

