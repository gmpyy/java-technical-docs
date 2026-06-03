---
title: React 渲染机制
description: 整理 React Element、虚拟 DOM、diff、key、Fiber、调和流程和性能优化策略。
outline: [2, 3]
---

# React 渲染机制

React 的渲染机制可以拆成三个层次：组件执行后得到 React Element；React 根据 React Element 构建 Fiber 树并进行调和；提交阶段把变化应用到真实 DOM。虚拟 DOM、diff、key 和 Fiber 都服务于同一个目标：让 UI 更新可预测、可中断、可优化。

## React Element 与虚拟 DOM

虚拟 DOM 不是浏览器里的 DOM，而是用 JavaScript 对象描述 UI 结构。JSX 最终会被编译成创建 React Element 的调用。React Element 是不可变描述，记录类型、props、key、ref 等信息。

```tsx
const element = (
  <button className="primary">
    保存
  </button>
)
```

可以把它理解成类似下面的结构：

```ts
const element = {
  type: 'button',
  key: null,
  ref: null,
  props: {
    className: 'primary',
    children: '保存'
  }
}
```

虚拟 DOM 主要做了三件事：

| 能力 | 说明 |
| --- | --- |
| 声明式描述 UI | 开发者只描述结果，不手动拼接 DOM 操作 |
| 跨平台抽象 | 同一套组件模型可以对应 DOM、Native、小程序等目标 |
| 支撑 diff | 新旧描述对象可比较，从而计算最小必要更新 |

虚拟 DOM 本身并不神奇，它是 React 调和算法的输入数据结构。React 真正的性能来自合理的更新粒度、diff 假设、事件批处理、Fiber 调度和跳过策略。

## 直接操作 DOM 与虚拟 DOM

直接操作原生 DOM 不一定总比虚拟 DOM 慢。对于一次明确的小改动，手写 DOM 可能更直接。但在复杂应用中，手写 DOM 需要开发者自己维护状态同步、节点复用、事件清理和边界情况，复杂度会迅速升高。

虚拟 DOM 的价值是把“从状态到界面”的过程标准化。开发者只更新状态，React 负责计算界面差异。它牺牲了一点运行时计算，换来可维护性、跨平台能力和一致的更新模型。

```tsx
function StatusLabel({ status }: { status: 'idle' | 'loading' | 'done' }) {
  return (
    <span data-status={status}>
      {status === 'loading' ? '加载中' : '完成'}
    </span>
  )
}
```

在这段代码中，开发者不需要知道文本节点、属性和 class 的具体 DOM 更新顺序。React 会根据前后 element 差异完成提交。

## diff 算法的核心假设

React diff 算法基于两个重要假设：

1. 不同类型的元素会产生不同树。
2. 同层级子元素可以通过 `key` 标识稳定身份。

这让 React 可以把复杂度从传统树比较的高成本降到更适合 UI 更新的同层比较。

```tsx
function Panel({ mode }: { mode: 'view' | 'edit' }) {
  if (mode === 'view') {
    return <article>展示内容</article>
  }

  return <form>编辑内容</form>
}
```

当根元素从 `article` 变成 `form`，React 会认为类型不同，直接替换对应子树。类型相同则保留 DOM 节点，更新属性和子节点。

```tsx
function Label({ active }: { active: boolean }) {
  return (
    <span className={active ? 'active' : 'normal'}>
      状态
    </span>
  )
}
```

这里根元素始终是 `span`，React 会复用原 DOM，只更新 `className`。

## key 的作用

`key` 用于帮助 React 在同层列表中识别元素身份。它不是传给组件的普通 props，而是调和阶段使用的标识。稳定 key 可以让 React 正确复用、移动或删除节点。

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

不要在会插入、删除、排序的列表中使用数组下标作为 key。下标 key 会把“位置”误当成“身份”，容易造成输入框内容串行、动画错乱或组件状态复用错误。

```tsx
// 不推荐：列表顺序变化时状态可能错位
items.map((item, index) => <TodoItem key={index} item={item} />)

// 推荐：使用业务唯一 id
items.map((item) => <TodoItem key={item.id} item={item} />)
```

key 主要解决的是同层子节点的身份识别问题。它不能阻止父组件渲染，也不能自动优化所有性能问题。

## 调和流程

React 的调和可以理解为“根据新旧元素描述计算 Fiber 树变化”。一次更新大致经历：

1. 触发更新：state、props、Context 或外部 store 变化。
2. render 阶段：执行组件函数或类组件 render，生成新 element。
3. reconcile 阶段：比较新旧结构，标记插入、更新、删除、副作用。
4. commit 阶段：把变化应用到宿主环境，并执行 layout effect、普通 effect 等。

```tsx
function App() {
  const [visible, setVisible] = React.useState(true)

  return (
    <>
      <button onClick={() => setVisible((value) => !value)}>
        切换
      </button>
      {visible ? <Message key="message" /> : null}
    </>
  )
}
```

render 阶段可以被打断、重启或丢弃；commit 阶段必须同步完成，因为真实 DOM 一旦开始修改，就需要保持一致。

## Fiber 的理解

Fiber 是 React 16 引入的新协调架构。它既是数据结构，也代表一种可中断、可恢复、可分片的渲染工作模型。每个组件、DOM 节点或文本节点都对应 Fiber 节点，Fiber 节点记录了类型、props、state、子节点、兄弟节点、父节点、更新队列、副作用标记等信息。

Fiber 解决的核心问题是：旧的递归渲染一旦开始，就难以中断。复杂页面更新可能长期占用主线程，导致输入、滚动和动画卡顿。Fiber 把渲染工作拆成一个个单元，让 React 能根据优先级调度任务，在必要时暂停低优先级工作，先响应高优先级交互。

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

这只是帮助理解的简化结构。真实 Fiber 结构更复杂。理解 Fiber 不需要记字段，而要掌握它带来的能力：

| 能力 | 说明 |
| --- | --- |
| 可中断渲染 | render 阶段可以拆分成工作单元 |
| 优先级调度 | 用户输入等高优先级任务可以先处理 |
| 双缓存树 | current 树和 work-in-progress 树交替工作 |
| 副作用收集 | 提交阶段集中处理 DOM 更新和 effect |
| 并发特性基础 | 支撑 transition、Suspense 等能力 |

## Fiber 与生命周期变化

Fiber 让 render 阶段可能被暂停、重启，因此旧的 `componentWillMount`、`componentWillReceiveProps`、`componentWillUpdate` 容易产生不安全副作用。它们可能被调用多次，但最终并不一定提交到界面。

这也是 React 推荐把副作用放到提交后的 `componentDidMount`、`componentDidUpdate`、`useEffect`，把 DOM 更新前快照放到 `getSnapshotBeforeUpdate` 的原因。

```tsx
class ScrollBox extends React.Component<{ items: string[] }> {
  private ref = React.createRef<HTMLDivElement>()

  getSnapshotBeforeUpdate(prevProps: { items: string[] }) {
    if (prevProps.items.length < this.props.items.length) {
      return this.ref.current?.scrollHeight ?? null
    }

    return null
  }

  componentDidUpdate(
    prevProps: { items: string[] },
    prevState: {},
    snapshot: number | null
  ) {
    if (snapshot !== null) {
      console.log('更新前高度', snapshot)
    }
  }

  render() {
    return <div ref={this.ref}>{this.props.items.join(',')}</div>
  }
}
```

## React 与 Vue diff 的不同

React 和 Vue 都使用虚拟 DOM，但实现细节和优化策略不同。

| 维度 | React | Vue |
| --- | --- | --- |
| 更新粒度 | 默认从触发更新的组件向下重新执行，依靠 memo、key、调和优化 | 响应式系统能更精确知道依赖，模板编译也能标记静态节点 |
| diff 假设 | 同层比较、类型不同替换、key 标识列表身份 | 同样重视 key，但结合模板编译生成优化信息 |
| 数据模型 | 单向数据流，状态变化触发组件渲染 | 响应式依赖收集，数据变化通知依赖更新 |
| 编译能力 | JSX 灵活，运行时判断更多 | 模板静态分析空间更大 |

两者没有绝对优劣。React 更强调 JavaScript 表达能力和组件函数模型；Vue 更强调模板约束带来的编译优化与细粒度响应式。

## 性能优化策略

React 性能优化应该遵循“先定位，再优化”。常见方向包括减少不必要渲染、降低单次渲染成本、切分长任务、延迟非关键内容和优化列表。

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

常见工具和场景如下：

| 工具 | 适合场景 |
| --- | --- |
| `React.memo` | props 稳定且子组件渲染成本较高 |
| `useMemo` | 昂贵计算或稳定对象引用 |
| `useCallback` | 稳定回调引用，配合 memo 子组件 |
| `PureComponent` | 类组件浅比较优化 |
| 虚拟列表 | 大量长列表渲染 |
| 组件拆分 | 缩小状态更新影响范围 |
| 懒加载 | 路由页、重组件、非首屏内容 |

过度优化会让代码复杂。比如所有函数都包 `useCallback`，可能只增加依赖维护成本。真正有效的优化通常来自更合理的状态位置和更小的渲染范围。

## 避免不必要 render

避免不必要 render 可以从数据设计开始。

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

如果 `ResultList` 很重，而输入过程中每次按键都会触发昂贵计算，可以拆分状态、做防抖、使用 `useDeferredValue` 或把结果计算放到服务端。不要只依赖 memo 掩盖数据流问题。

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

## 渲染机制检查清单

| 检查项 | 建议 |
| --- | --- |
| 列表 key | 使用稳定业务 id，不用易变化下标 |
| render 纯度 | 不在 render 中发请求、改 DOM、写外部状态 |
| 引用稳定性 | 需要时使用 `useMemo`、`useCallback` |
| 大列表 | 使用虚拟滚动或分页 |
| 重组件 | 使用懒加载、拆分、memo 和计算缓存 |
| Fiber 语义 | 副作用放到提交后阶段 |
| DOM 测量 | 使用 `useLayoutEffect` 或提交后的生命周期 |

