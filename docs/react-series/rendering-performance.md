---
title: React 渲染与性能
description: 整理 React render 原理、提高组件渲染效率、diff 原理、Fiber 架构和性能优化手段。
outline: [2, 3]
---

# React 渲染与性能

React 渲染与性能要从更新链路看：状态变化触发组件重新计算，React 生成新的 Element 树，调和阶段比较新旧结构，提交阶段把必要变化应用到真实 DOM。性能优化不是背 API，而是控制渲染范围、降低计算成本、稳定引用、优化列表和延迟非关键工作。

## React render 原理与触发时机

render 的本质是根据当前输入计算 UI 描述。函数组件是函数执行，类组件是调用 `render()` 方法。render 阶段不应该产生副作用，因为它可能被重新执行、打断或丢弃。

触发 render 的常见原因：

| 触发来源 | 说明 |
| --- | --- |
| state 更新 | `setState` 或 Hook setter |
| props 更新 | 父组件传入新 props |
| Context 更新 | Provider value 改变且组件读取该 Context |
| 外部 store 更新 | 绑定层订阅到外部状态变化 |
| forceUpdate | 类组件强制更新 |

```tsx
function Parent() {
  const [count, setCount] = React.useState(0)

  return (
    <>
      <button onClick={() => setCount((value) => value + 1)}>
        {count}
      </button>
      <Child label="固定文本" />
    </>
  )
}
```

父组件状态变化会让父组件重新执行。子组件是否重新执行，取决于组件结构、props 引用、memo 和调和结果。render 执行不等于真实 DOM 一定变化，DOM 变化发生在 commit 阶段。

## render 阶段与 commit 阶段

React 更新可以粗略分成两个阶段：

| 阶段 | 说明 | 能否被打断 |
| --- | --- | --- |
| render 阶段 | 执行组件，计算新树，标记变化 | 可以 |
| commit 阶段 | 修改 DOM，执行 layout effect 和生命周期 | 不应被打断 |

```tsx
function StatusLabel({ status }: {
  status: 'idle' | 'loading' | 'done'
}) {
  console.log('render status', status)

  React.useEffect(() => {
    console.log('committed status', status)
  }, [status])

  return <span>{status}</span>
}
```

日志可能帮助观察更新，但不要把业务副作用放在 render 中。请求、订阅、上报、DOM 读写应该放在 effect 或提交后的生命周期中。

## React diff 原理

React diff 原理基于两个假设：

1. 不同类型的元素会产生不同树。
2. 同层级子元素可以通过 `key` 标识稳定身份。

这个假设让 React 避免昂贵的任意树比较，把 UI 场景中的比较控制在更实用的范围内。

```tsx
function Panel({ mode }: { mode: 'view' | 'edit' }) {
  if (mode === 'view') {
    return <article>展示内容</article>
  }

  return <form>编辑内容</form>
}
```

当根元素从 `article` 变成 `form`，React 会认为类型不同，直接替换对应子树。类型相同则复用 DOM 节点并更新属性。

```tsx
function Label({ active }: { active: boolean }) {
  return (
    <span className={active ? 'active' : 'normal'}>
      状态
    </span>
  )
}
```

这里根元素始终是 `span`，React 只需要更新 `className`。

### 列表 diff 与 key

列表中，key 帮助 React 判断同层节点身份。

```tsx
function UserList({ users }: {
  users: Array<{ id: string; name: string }>
}) {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

稳定 key 可以让 React 正确复用、移动或删除节点。下标 key 在插入、删除、排序时容易造成组件状态错位。

## Fiber 架构

Fiber 架构是 React 16 引入的新协调架构。Fiber 既是一种数据结构，也是一种工作模型。每个组件、DOM 节点或文本节点都对应 Fiber 节点，节点上记录类型、props、state、子节点、兄弟节点、父节点、更新队列和副作用标记等信息。

```ts
type SimpleFiber = {
  type: unknown
  child: SimpleFiber | null
  sibling: SimpleFiber | null
  return: SimpleFiber | null
  pendingProps: unknown
  memoizedProps: unknown
  memoizedState: unknown
  flags: number
}
```

真实 Fiber 结构更复杂。理解 Fiber 不需要记字段，而要理解它带来的能力：

| 能力 | 说明 |
| --- | --- |
| 可中断渲染 | render 阶段可以拆成工作单元 |
| 优先级调度 | 用户输入等高优先级更新可以先处理 |
| 双缓存树 | current 树和 work-in-progress 树交替工作 |
| 副作用收集 | 提交阶段集中处理 DOM 更新和 effect |
| 并发基础 | 支撑 transition、Suspense、流式渲染等能力 |

Fiber 让 render 阶段可能被暂停、重启，因此旧的 render 前生命周期不适合放副作用。副作用要放在提交后阶段。

## 提高组件渲染效率

提高组件渲染效率可以从四个层面入手：

| 层面 | 方向 |
| --- | --- |
| 状态设计 | 状态放在真正需要它的最近位置 |
| 组件拆分 | 缩小更新影响范围 |
| 引用稳定 | 避免无意义对象、数组、函数引用变化 |
| 渲染成本 | 缓存昂贵计算、虚拟列表、懒加载 |

```tsx
const ExpensiveChart = React.memo(function ExpensiveChart(props: {
  data: number[]
}) {
  const points = React.useMemo(() => {
    return props.data.map((value, index) => ({ x: index, y: value }))
  }, [props.data])

  return <Chart points={points} />
})
```

`React.memo` 适合 props 稳定且渲染成本较高的组件。`useMemo` 适合缓存昂贵计算结果。`useCallback` 适合稳定回调引用，尤其是传给 memo 子组件时。

```tsx
const Row = React.memo(function Row(props: {
  id: string
  selected: boolean
  onSelect: (id: string) => void
}) {
  return (
    <button
      data-selected={props.selected}
      onClick={() => props.onSelect(props.id)}
    >
      {props.id}
    </button>
  )
})
```

如果父组件每次 render 都创建新的 `onSelect` 引用，`Row` 仍然会重新渲染。此时可以在父组件中使用 `useCallback`。

## 避免不必要 render

避免不必要 render 的关键不是把所有组件都 memo，而是让状态边界合理。

```tsx
function SearchPage() {
  const [keyword, setKeyword] = React.useState('')

  return (
    <>
      <SearchInput value={keyword} onChange={setKeyword} />
      <ResultList keyword={keyword} />
    </>
  )
}
```

如果 `ResultList` 很重，输入每次变化都会触发昂贵计算。可以使用防抖、`useDeferredValue`、服务端搜索或拆分计算。

```tsx
function SearchPage() {
  const [keyword, setKeyword] = React.useState('')
  const deferredKeyword = React.useDeferredValue(keyword)

  return (
    <>
      <SearchInput value={keyword} onChange={setKeyword} />
      <ResultList keyword={deferredKeyword} />
    </>
  )
}
```

`useDeferredValue` 不是跳过更新，而是允许低优先级内容延后更新，让输入保持响应。

## React 性能优化手段

React 性能优化手段可以按场景分类。

| 场景 | 手段 |
| --- | --- |
| 子组件重复执行 | `React.memo`、`PureComponent` |
| 昂贵计算 | `useMemo`、selector 缓存 |
| 回调引用变化 | `useCallback` |
| 大列表 | 虚拟滚动、分页、无限加载 |
| 路由包体大 | 懒加载和代码分割 |
| 非紧急更新 | transition、deferred value |
| 服务端首屏 | SSR、流式渲染、缓存 |
| 图片和静态资源 | 懒加载、尺寸约束、预加载关键资源 |

路由级懒加载示例：

```tsx
const SettingsPage = React.lazy(() => import('./SettingsPage'))

function AppRoutes() {
  return (
    <React.Suspense fallback={<span>加载中...</span>}>
      <SettingsPage />
    </React.Suspense>
  )
}
```

长列表示意：

```tsx
function VisibleRows({ rows, start, end }: {
  rows: Array<{ id: string; title: string }>
  start: number
  end: number
}) {
  return (
    <>
      {rows.slice(start, end).map((row) => (
        <Row key={row.id} id={row.id} title={row.title} />
      ))}
    </>
  )
}
```

真实项目可使用成熟虚拟列表库。核心思想是只渲染视口附近的元素，而不是一次性渲染全部数据。

## PureComponent 与 shouldComponentUpdate

类组件中，`PureComponent` 内置浅比较，`shouldComponentUpdate` 可以自定义是否更新。

```tsx
class PriceLabel extends React.PureComponent<{
  amount: number
  currency: string
}> {
  render() {
    return <span>{this.props.currency} {this.props.amount}</span>
  }
}
```

浅比较依赖不可变更新。如果直接修改对象或数组引用，React 可能误判没有变化。

```tsx
class UserRow extends React.Component<{
  id: string
  selected: boolean
}> {
  shouldComponentUpdate(nextProps: { id: string; selected: boolean }) {
    return nextProps.selected !== this.props.selected
  }

  render() {
    return <li aria-selected={this.props.selected}>{this.props.id}</li>
  }
}
```

函数组件中对应工具是 `React.memo`。不过任何跳过策略都应建立在性能定位基础上，避免为了优化引入更高维护成本。

## React 与 Vue diff 的差异

React 和 Vue 都使用虚拟 DOM，但优化方向不同。

| 维度 | React | Vue |
| --- | --- | --- |
| 更新来源 | 状态变化触发组件重新执行 | 响应式依赖追踪更细 |
| 编译能力 | JSX 灵活，运行时判断更多 | 模板约束便于静态分析 |
| 优化手段 | memo、key、Fiber、调度 | patch flag、静态提升、依赖收集 |
| 数据流 | 单向数据流更突出 | 响应式模型更直接 |

两者没有绝对优劣。React 更强调 JavaScript 表达能力和组件函数模型；Vue 更强调模板约束与细粒度响应式。

## 渲染与性能检查清单

| 检查项 | 建议 |
| --- | --- |
| render 纯度 | 不在 render 中发请求、写外部状态、读写 DOM |
| state 位置 | 状态放在最近共同使用处 |
| props 引用 | 传给 memo 子组件的对象、数组、函数保持必要稳定 |
| key | 使用稳定业务 id，避免下标 key |
| 大列表 | 使用分页、虚拟滚动或服务端过滤 |
| 昂贵计算 | 用 `useMemo` 或 selector 缓存 |
| 包体 | 使用懒加载和代码分割 |
| Fiber 语义 | 副作用放到提交后阶段 |

