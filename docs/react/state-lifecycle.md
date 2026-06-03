---
title: React 状态与生命周期
description: 整理 setState、props、state、PropTypes、生命周期迁移、渲染更新流程和数据请求位置。
outline: [2, 3]
---

# React 状态与生命周期

状态管理是 React 组件工作的核心。props 表示外部传入的数据，state 表示组件自身维护的数据；props 改变和 state 改变都会让 React 重新计算界面描述，再进入调和与提交流程。类组件时代，这些变化通常和生命周期方法绑定；函数组件时代，生命周期语义被拆成了渲染、提交、副作用和清理。

## state 与 props

`props` 是父组件传给子组件的只读输入，`state` 是组件内部维护的可变数据。这里的“可变”不是指可以直接修改对象，而是指组件可以通过 React 提供的更新入口发起变化。

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

props 之所以应该只读，是因为 React 使用单向数据流保证变化来源清晰。如果子组件直接修改 props，父组件并不知道这个变化，调试和同步都会变得混乱。需要修改时，应让父组件传入回调或把状态提升到共同父级。

| 项目 | props | state |
| --- | --- | --- |
| 来源 | 父组件或外部调用方 | 组件自身 |
| 是否只读 | 对当前组件只读 | 通过更新函数改变 |
| 典型用途 | 配置、数据输入、回调 | 交互状态、局部缓存、临时 UI 状态 |
| 变化影响 | 子组件重新渲染 | 当前组件及相关子树重新渲染 |

## setState 调用原理

类组件的 `setState` 并不是简单地直接改写 `this.state`。调用后，React 会创建一次更新，把更新内容放入对应 Fiber 节点的更新队列中，然后根据当前优先级安排渲染。

```tsx
class Counter extends React.Component<{}, { count: number }> {
  state = {
    count: 0
  }

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

`setState` 的对象写法适合不依赖旧状态的更新；函数写法适合依赖旧状态的更新。连续更新同一个字段时，应使用函数写法，避免读取到旧的闭包值或旧的 `this.state`。

```tsx
this.setState((state) => ({ count: state.count + 1 }))
this.setState((state) => ({ count: state.count + 1 }))
```

这类更新会进入队列，React 按顺序计算最终 state。理解这一点，可以避免把 `setState` 误解成同步赋值语句。

## setState 之后发生什么

调用 `setState` 后，React 通常会经历这些步骤：

1. 创建 update 对象，记录 payload、callback、优先级等信息。
2. 把 update 挂到当前 Fiber 的更新队列。
3. 从当前 Fiber 向上找到根节点，安排一次更新任务。
4. 在渲染阶段计算新状态，执行组件渲染，生成新的 Fiber 树。
5. 在提交阶段把变化应用到 DOM，并执行相关生命周期或 effect。
6. 如果传入了 `setState` 第二个参数回调，在提交后执行。

```tsx
this.setState(
  { saved: true },
  () => {
    console.log('DOM 已经按新状态提交')
  }
)
```

函数组件中没有 `setState` 第二个参数。如果需要在状态提交后执行副作用，应使用 `useEffect` 监听状态。

```tsx
function SaveStatus() {
  const [saved, setSaved] = React.useState(false)

  React.useEffect(() => {
    if (saved) {
      console.log('保存状态已提交到界面')
    }
  }, [saved])

  return <button onClick={() => setSaved(true)}>保存</button>
}
```

## setState 是同步还是异步

更准确的说法是：`setState` 是“请求一次状态更新”，不是立即赋值。React 会根据执行环境、版本和批处理策略决定何时刷新。

在 React 18 的自动批处理中，同一次事件、Promise、定时器等上下文里的多个状态更新可以被合并，减少重复渲染。开发者不应该依赖调用后立刻读取到新 state。

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

批量更新不是“丢失更新”。React 会把多个 update 合并进一次渲染任务，最终状态仍按更新队列计算。只有直接读取旧值再多次对象写法覆盖同一字段时，才容易出现结果不符合预期。

## 批量更新过程

批量更新可以理解为“收集更新，再统一计算”。同一批次内，多次更新先进入队列；渲染时，React 从基础 state 开始，依次应用队列中的每个 update，得到新 state，再执行 render。

```tsx
class BatchCounter extends React.Component<{}, { count: number }> {
  state = { count: 0 }

  addTwice = () => {
    this.setState((state) => ({ count: state.count + 1 }))
    this.setState((state) => ({ count: state.count + 1 }))
  }

  render() {
    return <button onClick={this.addTwice}>{this.state.count}</button>
  }
}
```

这段代码每次点击会增加 2。若写成两次 `{ count: this.state.count + 1 }`，两次读取的可能是同一个旧值，最终只增加 1。

## this.state 与 setState

`this.state` 是当前渲染快照中的状态对象，`setState` 是通知 React 安排更新的入口。直接写 `this.state.count++` 不会触发渲染，也可能破坏 React 对更新前后引用的判断。

```tsx
// 不推荐
this.state.count = this.state.count + 1

// 推荐
this.setState((state) => ({
  count: state.count + 1
}))
```

初始化状态可以直接赋值，因为此时组件还没有进入更新流程。

```tsx
class UserPanel extends React.Component<{}, { name: string }> {
  state = {
    name: ''
  }

  render() {
    return <input value={this.state.name} onChange={() => {}} />
  }
}
```

## replaceState

`replaceState` 是早期 React 中替换整个 state 的方式，现代项目很少使用。`setState` 在类组件中会浅合并对象更新，而 `replaceState` 是整体替换，因此容易丢失未写入的字段。

```tsx
// 假设当前 state 为 { name: 'Lin', age: 18 }
this.setState({ name: 'Chen' })
// 结果类似 { name: 'Chen', age: 18 }

// 旧 API 的整体替换思路会丢失 age
// replaceState({ name: 'Chen' })
```

函数组件的 `useState` setter 不会自动浅合并对象；它更接近“替换当前状态值”。如果状态是对象，需要手动展开旧对象。

```tsx
const [form, setForm] = React.useState({ name: '', age: 0 })

setForm((prev) => ({
  ...prev,
  name: 'Chen'
}))
```

## getDefaultProps

`getDefaultProps` 是 `React.createClass` 时代设置默认 props 的方式。现代代码中，函数组件可以使用参数默认值，类组件可以使用 `defaultProps` 或调用方兜底。

```tsx
type ButtonProps = {
  size?: 'small' | 'medium' | 'large'
}

function Button({ size = 'medium' }: ButtonProps) {
  return <button data-size={size}>按钮</button>
}
```

如果维护旧代码，看到 `getDefaultProps` 时要知道它用于定义 props 默认值，并且只会创建一次默认对象。涉及可变引用时要特别谨慎。

## props 改变后的处理方式

props 改变时，不应该无条件把 props 拷贝到 state。只有当组件确实需要维护“派生状态”时，才考虑使用 `getDerivedStateFromProps` 或在 effect 中响应变化。

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

函数组件中，可以用 `useEffect` 响应 props 变化，但也要先问清楚是否真的需要本地副本。

```tsx
function KeywordInput({ keyword }: { keyword: string }) {
  const [draft, setDraft] = React.useState(keyword)

  React.useEffect(() => {
    setDraft(keyword)
  }, [keyword])

  return <input value={draft} onChange={(event) => setDraft(event.target.value)} />
}
```

如果只是根据 props 计算展示值，优先在渲染时直接计算或用 `useMemo` 缓存，避免制造多份状态。

## state 从 reducer 到组件的过程

在 Redux 这类状态管理中，状态通常从 reducer 产生，再通过 store、订阅机制和连接层注入组件。流程可以概括为：组件 dispatch action，store 调用 reducer 产生新 state，订阅者收到通知，连接层选择需要的片段，再作为 props 传给组件。

```tsx
type State = {
  count: number
}

type Action = {
  type: 'increase'
}

function reducer(state: State = { count: 0 }, action: Action): State {
  switch (action.type) {
    case 'increase':
      return { count: state.count + 1 }
    default:
      return state
  }
}
```

组件感知到的仍然是 props 更新。Redux 并不是绕开 React 更新机制，而是把外部 store 的变化映射成组件输入变化。

## Props 校验与 PropTypes

React 可以通过 PropTypes 做运行时 props 校验。TypeScript 提供编译期类型检查，但在纯 JavaScript 项目、组件库边界或需要运行时兜底时，PropTypes 仍然有意义。

```tsx
import PropTypes from 'prop-types'

function UserCard(props: { name: string; age?: number }) {
  return (
    <article>
      <h3>{props.name}</h3>
      <p>{props.age}</p>
    </article>
  )
}

UserCard.propTypes = {
  name: PropTypes.string.isRequired,
  age: PropTypes.number
}
```

验证 props 的目的不是让代码变啰嗦，而是尽早暴露调用错误：字段缺失、类型不一致、枚举值错误、回调未传等问题，都能在开发阶段更快发现。

## 生命周期总览

类组件生命周期可以按阶段理解。

| 阶段 | 主要方法 | 说明 |
| --- | --- | --- |
| 挂载 | `constructor`、`render`、`componentDidMount` | 初始化并插入 DOM |
| 更新 | `getDerivedStateFromProps`、`shouldComponentUpdate`、`render`、`getSnapshotBeforeUpdate`、`componentDidUpdate` | props 或 state 变化后重新渲染 |
| 卸载 | `componentWillUnmount` | 清理订阅、定时器和外部资源 |
| 错误 | `getDerivedStateFromError`、`componentDidCatch` | 错误边界处理子树异常 |

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

生命周期的核心原则是：render 负责纯计算，提交后的方法负责 DOM、订阅、网络和其他副作用。

## 被废弃或不推荐的生命周期

React 不再推荐直接使用 `componentWillMount`、`componentWillReceiveProps`、`componentWillUpdate`。它们在异步渲染和 Fiber 调度下容易被多次调用、被打断或产生副作用不一致的问题。新版本中可以看到 `UNSAFE_` 前缀，这是提醒开发者迁移。

| 旧方法 | 常见替代 |
| --- | --- |
| `componentWillMount` | constructor、`componentDidMount`、函数组件初始化 |
| `componentWillReceiveProps` | `getDerivedStateFromProps`、`componentDidUpdate`、`useEffect` |
| `componentWillUpdate` | `getSnapshotBeforeUpdate`、`componentDidUpdate` |

`componentWillReceiveProps` 的典型用途是 props 变化时同步内部状态或发起副作用。但在现代代码中，要区分两类需求：派生状态用 `getDerivedStateFromProps`，副作用用 `componentDidUpdate` 或 `useEffect`。

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

## React 16 后的新生命周期

React 16 引入并强调了两个生命周期：`getDerivedStateFromProps` 和 `getSnapshotBeforeUpdate`。

`getDerivedStateFromProps` 是静态方法，不能访问实例 `this`，适合根据 props 和旧 state 计算新的派生 state。它应该保持纯函数，不要发请求、订阅或操作 DOM。

`getSnapshotBeforeUpdate` 在 DOM 更新前调用，返回值会作为第三个参数传给 `componentDidUpdate`，适合读取滚动位置等更新前快照。

```tsx
class MessageList extends React.Component<
  { messages: string[] },
  {}
> {
  private listRef = React.createRef<HTMLDivElement>()

  getSnapshotBeforeUpdate(prevProps: { messages: string[] }) {
    if (prevProps.messages.length < this.props.messages.length) {
      const list = this.listRef.current
      return list ? list.scrollHeight - list.scrollTop : null
    }

    return null
  }

  componentDidUpdate(
    prevProps: { messages: string[] },
    prevState: {},
    snapshot: number | null
  ) {
    if (snapshot !== null && this.listRef.current) {
      this.listRef.current.scrollTop = this.listRef.current.scrollHeight - snapshot
    }
  }

  render() {
    return (
      <div ref={this.listRef}>
        {this.props.messages.map((message) => <p key={message}>{message}</p>)}
      </div>
    )
  }
}
```

## 性能优化生命周期

类组件中的 `shouldComponentUpdate` 是主要性能优化入口。它通过比较新旧 props 和 state 决定是否跳过当前组件的渲染。

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

优化原理很直接：如果组件输出不会因为本次输入变化而改变，就跳过它和子树的渲染计算。函数组件对应的工具是 `React.memo`，计算缓存是 `useMemo`，回调缓存是 `useCallback`。

## state 和 props 触发更新的差异

state 更新从组件自身发起，props 更新从父组件传入。两者都会让组件进入更新流程，但追踪问题时关注点不同：

| 来源 | 追踪方向 | 常见问题 |
| --- | --- | --- |
| state | 看组件内部事件、副作用、定时器、请求回调 | 直接修改状态、闭包旧值、批处理误解 |
| props | 向上查父组件渲染和传参 | 新对象引用过多、派生状态重复、回调未缓存 |

如果 props 和 state 同时变化，React 会在同一次渲染中计算最终结果。不要依赖某个生命周期中“先看到谁变化”，应该基于当前 props/state 的最终值写逻辑。

## 网络请求放在哪里

类组件中，首次网络请求通常放在 `componentDidMount`，因为这个阶段组件已经挂载，副作用不会污染 render，也能在卸载时取消订阅或忽略过期结果。props 变化引发的新请求放在 `componentDidUpdate`，并与旧 props 比较。

```tsx
class UserProfile extends React.Component<
  { userId: string },
  { name: string }
> {
  state = { name: '' }

  componentDidMount() {
    this.loadUser(this.props.userId)
  }

  componentDidUpdate(prevProps: { userId: string }) {
    if (prevProps.userId !== this.props.userId) {
      this.loadUser(this.props.userId)
    }
  }

  async loadUser(userId: string) {
    const user = await fetchUser(userId)
    this.setState({ name: user.name })
  }

  render() {
    return <h2>{this.state.name}</h2>
  }
}
```

函数组件中，对应写法是 `useEffect`。

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [name, setName] = React.useState('')

  React.useEffect(() => {
    let ignore = false

    fetchUser(userId).then((user) => {
      if (!ignore) {
        setName(user.name)
      }
    })

    return () => {
      ignore = true
    }
  }, [userId])

  return <h2>{name}</h2>
}
```

这里的 `ignore` 用于避免旧请求在组件卸载或参数变化后继续写入状态。真实项目中也可以使用 `AbortController`。

## 生命周期迁移到 Hooks

Hooks 不是把每个生命周期机械改名，而是把逻辑按用途重新组织。

| class 生命周期 | Hook 表达 |
| --- | --- |
| `componentDidMount` | `useEffect(() => {}, [])` |
| `componentDidUpdate` | `useEffect(() => {}, [deps])` |
| `componentWillUnmount` | effect 返回清理函数 |
| `shouldComponentUpdate` | `React.memo`、`useMemo`、`useCallback` |
| `getSnapshotBeforeUpdate` | `useLayoutEffect` 配合 ref |
| `componentDidCatch` | 仍主要使用类组件错误边界，或框架提供封装 |

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

迁移时不要把一个大生命周期函数原封不动塞进一个大 `useEffect`。更好的方式是按订阅、请求、标题同步、埋点等副作用类型拆分多个 effect。

## 状态与生命周期检查清单

| 检查项 | 建议 |
| --- | --- |
| 更新依赖旧状态 | 使用函数式更新 |
| 需要提交后回调 | 类组件用 `setState` 第二参数，函数组件用 `useEffect` |
| props 派生 state | 先判断是否真的需要本地副本 |
| 网络请求 | 放在提交后的生命周期或 effect |
| 性能优化 | 先定位瓶颈，再使用 `shouldComponentUpdate`、`PureComponent`、`React.memo` |
| 卸载清理 | 清理定时器、订阅、事件监听和过期请求 |
| 旧生命周期 | 优先迁移到新生命周期或 Hooks 表达 |

