---
title: React 状态与生命周期
description: 整理 React 生命周期阶段、state 与 props、super(props)、setState 执行机制和 render 触发时机。
outline: [2, 3]
---

# React 状态与生命周期

状态与生命周期描述的是 React 组件如何接收输入、保存内部数据、触发更新、处理副作用和释放资源。类组件时代，这些能力集中在生命周期方法和 `setState` 中；函数组件时代，它们被拆成渲染、提交、effect、清理和 Hook 状态单元。

## state 与 props

state 与 props 的区别是理解 React 数据流的第一步。

| 项目 | props | state |
| --- | --- | --- |
| 来源 | 父组件、路由、外部调用方 | 组件自身 |
| 是否可直接修改 | 当前组件只读 | 通过更新入口修改 |
| 典型用途 | 配置、数据输入、回调函数 | 交互状态、局部缓存、临时 UI 状态 |
| 变化影响 | 子组件重新计算输出 | 当前组件及相关子树重新计算输出 |

```tsx
function Greeting(props: { name: string }) {
  const [visible, setVisible] = React.useState(true)

  if (!visible) {
    return null
  }

  return (
    <p onClick={() => setVisible(false)}>
      你好，{props.name}
    </p>
  )
}
```

props 应保持只读。如果子组件直接修改 props，父组件无法感知变化，数据来源会变得混乱。需要修改父级数据时，应由父组件传入回调。

```tsx
function Parent() {
  const [name, setName] = React.useState('Lin')

  return <NameEditor name={name} onNameChange={setName} />
}
```

不要无条件把 props 拷贝到 state。只有组件确实需要维护“本地草稿”或“派生快照”时，才考虑这么做。

## React 生命周期阶段

类组件生命周期可以按阶段理解：

| 阶段 | 主要方法 | 关注点 |
| --- | --- | --- |
| 挂载 | `constructor`、`render`、`componentDidMount` | 初始化、首次插入 DOM、启动副作用 |
| 更新 | `getDerivedStateFromProps`、`shouldComponentUpdate`、`render`、`getSnapshotBeforeUpdate`、`componentDidUpdate` | 根据新 props/state 重新计算和提交 |
| 卸载 | `componentWillUnmount` | 清理订阅、定时器、请求和外部资源 |
| 错误 | `getDerivedStateFromError`、`componentDidCatch` | 捕获子树渲染错误并降级展示 |

```tsx
class Timer extends React.Component<{}, { seconds: number }> {
  state = { seconds: 0 }
  private timer: number | undefined

  componentDidMount() {
    this.timer = window.setInterval(() => {
      this.setState((state) => ({ seconds: state.seconds + 1 }))
    }, 1000)
  }

  componentWillUnmount() {
    window.clearInterval(this.timer)
  }

  render() {
    return <span>{this.state.seconds}</span>
  }
}
```

render 阶段应该保持纯计算，不发请求、不订阅、不改 DOM。副作用放在提交后的生命周期或 effect 中。

### 不推荐的旧生命周期

`componentWillMount`、`componentWillReceiveProps`、`componentWillUpdate` 不再推荐使用。Fiber 架构下，render 阶段可能被打断、重启或丢弃，这些方法中的副作用可能执行多次却没有最终提交。

| 旧方法 | 迁移方向 |
| --- | --- |
| `componentWillMount` | constructor、`componentDidMount`、函数组件初始化 |
| `componentWillReceiveProps` | `getDerivedStateFromProps`、`componentDidUpdate`、`useEffect` |
| `componentWillUpdate` | `getSnapshotBeforeUpdate`、`componentDidUpdate` |

```tsx
class SearchResult extends React.Component<{ keyword: string }> {
  componentDidUpdate(prevProps: { keyword: string }) {
    if (prevProps.keyword !== this.props.keyword) {
      this.loadData(this.props.keyword)
    }
  }

  loadData(keyword: string) {
    console.log('load', keyword)
  }

  render() {
    return <div>{this.props.keyword}</div>
  }
}
```

## super() 与 super(props)

`super()` 与 `super(props)` 来自 ES class 继承。子类构造函数中必须先调用 `super()`，才能访问 `this`。React 类组件继承自 `React.Component`，因此写 constructor 时也必须先调用父类构造函数。

```tsx
class UserPanel extends React.Component<{ name: string }> {
  constructor(props: { name: string }) {
    super(props)
    console.log(this.props.name)
  }

  render() {
    return <p>{this.props.name}</p>
  }
}
```

区别在于：`super(props)` 会把 props 传给父类构造函数，让 constructor 内部可以通过 `this.props` 访问 props；`super()` 只完成父类初始化，constructor 中的 `this.props` 不可靠。

```tsx
class BadPanel extends React.Component<{ name: string }> {
  constructor(props: { name: string }) {
    super()
    // 这里不应依赖 this.props
    console.log(props.name)
  }

  render() {
    return <p>{this.props.name}</p>
  }
}
```

即使 constructor 中没有传 props，React 后续仍会把 props 挂到实例上，所以 render 中通常能访问 `this.props`。但实践中写 constructor 时统一使用 `super(props)` 更清晰、更稳妥。

constructor 只在需要初始化 state、绑定方法或创建实例字段时使用。现代 class 组件可以用类字段初始化 state，函数组件则用 `useState`。

## setState 执行机制

类组件的 `setState` 不是立即修改 `this.state` 的赋值语句，而是提交一次更新请求。React 会创建 update，把它放入当前 Fiber 的更新队列，并按优先级安排渲染。

```tsx
class Counter extends React.Component<{}, { count: number }> {
  state = { count: 0 }

  increase = () => {
    this.setState((prevState) => ({
      count: prevState.count + 1
    }))
  }

  render() {
    return <button onClick={this.increase}>{this.state.count}</button>
  }
}
```

对象写法适合不依赖旧状态的更新；函数写法适合依赖旧状态的更新。

```tsx
this.setState((state) => ({ count: state.count + 1 }))
this.setState((state) => ({ count: state.count + 1 }))
```

上面两次更新会按队列顺序计算，最终增加 2。若写成两次 `{ count: this.state.count + 1 }`，两次读取到的可能是同一个旧快照，结果不符合预期。

### setState 后发生什么

一次 `setState` 通常经历这些步骤：

1. 创建 update 对象，记录更新内容、回调和优先级。
2. 把 update 加入对应 Fiber 的更新队列。
3. 从当前 Fiber 向上找到根节点，安排更新任务。
4. 渲染阶段计算新状态并执行 render。
5. 调和阶段生成需要提交的变化。
6. 提交阶段更新 DOM 并执行生命周期或 effect。
7. 如果类组件传入第二个参数回调，提交后执行回调。

```tsx
this.setState(
  { saved: true },
  () => {
    console.log('界面已经提交保存状态')
  }
)
```

函数组件没有 `setState` 第二个参数。需要在状态提交后执行副作用时，用 `useEffect` 监听依赖。

```tsx
function SaveStatus() {
  const [saved, setSaved] = React.useState(false)

  React.useEffect(() => {
    if (saved) {
      console.log('保存状态已提交')
    }
  }, [saved])

  return <button onClick={() => setSaved(true)}>保存</button>
}
```

## 批处理与同步感知

更准确的表达是：`setState` 是请求一次更新，而不是立即赋值。React 会根据执行环境、版本和优先级决定何时刷新。

React 18 的自动批处理会把同一事件、Promise、定时器等上下文中的多次状态更新合并成更少的渲染。

```tsx
function BatchDemo() {
  const [count, setCount] = React.useState(0)
  const [flag, setFlag] = React.useState(false)

  function handleClick() {
    setCount((value) => value + 1)
    setFlag((value) => !value)
  }

  return <button onClick={handleClick}>{count} - {String(flag)}</button>
}
```

批处理不会丢失更新。真正容易出错的是把旧快照当作最新状态使用。依赖旧状态时使用函数式更新，可以避开这类问题。

## render 原理与触发时机

render 的职责是根据当前 props、state 和 context 计算 UI 描述。触发 render 的常见原因包括：

| 触发来源 | 说明 |
| --- | --- |
| state 更新 | 类组件 `setState`，函数组件状态 setter |
| props 更新 | 父组件重新渲染并传入新 props |
| Context 更新 | 组件读取的 Context value 变化 |
| 外部 store 更新 | 绑定层把外部状态变化转成组件输入变化 |
| forceUpdate | 类组件强制进入更新流程 |

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

父组件状态变化后，父组件函数会重新执行。子组件是否重新执行，取决于组件结构、memo、props 引用和调和结果。即使子组件 props 看起来没变，父组件重新执行时也可能带动子组件执行。

## props 改变后的处理方式

props 变化时，不应默认同步到 state。更好的判断方式是先问：这个值是否真的需要被用户本地编辑、延迟提交或与来源分离？

```tsx
class KeywordInput extends React.Component<
  { keyword: string },
  { draft: string; prevKeyword: string }
> {
  state = {
    draft: this.props.keyword,
    prevKeyword: this.props.keyword
  }

  static getDerivedStateFromProps(
    nextProps: { keyword: string },
    prevState: { draft: string; prevKeyword: string }
  ) {
    if (nextProps.keyword !== prevState.prevKeyword) {
      return {
        draft: nextProps.keyword,
        prevKeyword: nextProps.keyword
      }
    }

    return null
  }

  render() {
    return <input value={this.state.draft} onChange={() => {}} />
  }
}
```

函数组件中可以用 effect 响应 props 变化，但同样要确认是否需要本地副本。

```tsx
function KeywordInput({ keyword }: { keyword: string }) {
  const [draft, setDraft] = React.useState(keyword)

  React.useEffect(() => {
    setDraft(keyword)
  }, [keyword])

  return (
    <input
      value={draft}
      onChange={(event) => setDraft(event.target.value)}
    />
  )
}
```

如果只是根据 props 计算展示值，优先在 render 中直接计算，或用 `useMemo` 缓存昂贵计算。

## 网络请求放在哪里

类组件首次请求通常放在 `componentDidMount`，参数变化引发的新请求放在 `componentDidUpdate`。函数组件用 `useEffect` 表达同样语义。

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [name, setName] = React.useState('')

  React.useEffect(() => {
    let active = true

    fetchUser(userId).then((user) => {
      if (active) {
        setName(user.name)
      }
    })

    return () => {
      active = false
    }
  }, [userId])

  return <h2>{name}</h2>
}
```

这里的 `active` 用于忽略过期结果。真实项目也可以使用 `AbortController` 取消请求。

## 生命周期迁移到 Hooks

Hooks 不是生命周期方法的机械改名，而是按副作用目的重新组织代码。

| class 需求 | Hook 表达 |
| --- | --- |
| 挂载后执行 | `useEffect(() => {}, [])` |
| 参数变化后执行 | `useEffect(() => {}, [deps])` |
| 卸载清理 | effect 返回清理函数 |
| DOM 测量 | `useLayoutEffect` |
| 性能跳过 | `React.memo`、`useMemo`、`useCallback` |
| 错误边界 | 仍以类组件或框架封装为主 |

```tsx
function WindowSize() {
  const [size, setSize] = React.useState({
    width: window.innerWidth,
    height: window.innerHeight
  })

  React.useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      })
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return <span>{size.width} x {size.height}</span>
}
```

迁移时应拆分副作用，而不是把一个巨大的生命周期函数塞进一个巨大的 `useEffect`。

## 状态与生命周期检查清单

| 检查项 | 建议 |
| --- | --- |
| state 与 props | props 只读，state 通过 React 更新入口改变 |
| constructor | 需要时使用，并写 `super(props)` |
| setState | 依赖旧状态时使用函数式更新 |
| 批处理 | 不依赖调用后立即读取到新状态 |
| render | 保持纯计算，不发请求、不改 DOM |
| props 派生 state | 先确认是否真的需要本地副本 |
| 生命周期 | 副作用放到提交后阶段 |
| 清理 | 卸载或依赖变化时清理订阅、定时器、请求和事件 |

