---
title: React 技术文档
description: 从组件、状态、生命周期、Hooks、渲染机制、路由、状态管理到工程实践的 React 系统化文档。
outline: [2, 3]
---

# React 技术文档

这套文档把 React 常用知识整理成面向开发落地的技术资料。写法不采用问答列表，而是按“概念、原理、用法、注意点、代码示例、实践建议”的顺序展开，方便在真实项目中查阅、复盘和补齐知识结构。

React 的核心思想可以概括为：用组件描述 UI，用状态驱动视图变化，用单向数据流降低复杂度，用声明式写法隐藏 DOM 操作细节。当应用变大后，还需要理解事件系统、更新调度、Fiber、diff、Hooks、路由、状态管理和工程组织方式。

```tsx
import { useState } from 'react'

export function CounterPanel() {
  const [count, setCount] = useState(0)

  return (
    <section>
      <h2>当前计数：{count}</h2>
      <button onClick={() => setCount((value) => value + 1)}>
        增加
      </button>
    </section>
  )
}
```

上面这段代码体现了 React 的基本工作方式：组件返回 React Element，事件触发状态更新，React 根据新旧描述计算变化，再把结果提交到真实界面。

## 阅读路径

如果你刚接触 React，可以按下面顺序阅读：

1. 先看组件基础，理解组件、元素、实例、事件、refs、Context、受控组件与非受控组件。
2. 再看状态与生命周期，掌握 `setState`、props、状态更新流程、生命周期迁移和数据请求位置。
3. 接着看 Hooks，理解函数组件时代如何复用状态逻辑和副作用逻辑。
4. 然后看渲染机制，补上虚拟 DOM、diff、key、Fiber 和性能优化的底层图景。
5. 最后看通信、路由、Redux 与工程实践，把知识放到真实项目结构中。

## 章节地图

| 章节 | 内容范围 |
| --- | --- |
| 组件基础 | 事件机制、组件声明、HOC、Render props、PureComponent、Fragment、refs、Portals、Context、受控与非受控组件 |
| 状态与生命周期 | `setState` 原理、批量更新、props/state、PropTypes、旧生命周期迁移、React 16 后的生命周期 |
| Hooks | `useState`、`useEffect`、`useLayoutEffect`、`useMemo`、`useCallback`、`useRef`、自定义 Hook、闭包与依赖 |
| 渲染机制 | React Element、虚拟 DOM、diff、key、Fiber、调和、提交阶段、性能优化 |
| 通信、路由与状态管理 | 父子通信、跨级通信、发布订阅、React-Router、Redux、middleware、connect、MobX、Vuex |
| 工程实践 | 命名、版本演进、全局弹窗、持久化、TypeScript、JSX、SSR、严格模式、React.Children、高阶组件设计模式 |

## 知识覆盖表

| 原始主题 | 本文档位置 |
| --- | --- |
| 组件基础 | [组件基础](/react/component-basics) |
| 数据管理 | [状态与生命周期](/react/state-lifecycle) |
| 生命周期 | [状态与生命周期](/react/state-lifecycle) |
| 组件通信 | [通信、路由与状态管理](/react/router-state) |
| 路由 | [通信、路由与状态管理](/react/router-state) |
| Redux | [通信、路由与状态管理](/react/router-state) |
| Hooks | [Hooks](/react/hooks) |
| 虚拟 DOM | [渲染机制](/react/rendering) |
| 其他实践主题 | [工程实践](/react/ecosystem-practice) |

## 关键心智模型

### 组件是 UI 的函数

函数组件最直观，输入是 props，输出是 React Element。类组件也遵循同样的描述式模型，只是它把状态、生命周期和实例方法挂在 class 实例上。

```tsx
type UserCardProps = {
  name: string
  role: string
}

export function UserCard({ name, role }: UserCardProps) {
  return (
    <article>
      <h3>{name}</h3>
      <p>{role}</p>
    </article>
  )
}
```

### 状态改变才会驱动视图改变

不要直接修改状态对象。React 需要通过状态更新入口知道“组件需要重新计算视图”。类组件中使用 `setState`，函数组件中使用 Hook 返回的 setter。

```tsx
function TodoToggle() {
  const [done, setDone] = useState(false)

  return (
    <label>
      <input
        type="checkbox"
        checked={done}
        onChange={(event) => setDone(event.target.checked)}
      />
      已完成
    </label>
  )
}
```

### 单向数据流让变化可追踪

父组件把数据传给子组件，子组件通过回调把用户动作传回父组件。复杂场景可以把共享状态提升到共同父级、Context、Redux 或其他状态层中。

```tsx
function Parent() {
  const [keyword, setKeyword] = useState('')

  return (
    <SearchBox
      value={keyword}
      onChange={setKeyword}
    />
  )
}

function SearchBox(props: {
  value: string
  onChange: (value: string) => void
}) {
  return (
    <input
      value={props.value}
      onChange={(event) => props.onChange(event.target.value)}
    />
  )
}
```

## 资源说明

本 React 分区不依赖远端图片。源材料中的站点头像、页面装饰、二维码和评论区资源不属于正文技术内容，因此没有纳入文档站。后续如果补充真正的技术图示，应放入 `docs/public/images/react/`，并在 Markdown 中使用 `/images/react/...` 形式引用。

