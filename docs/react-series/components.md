---
title: React 组件系统
description: 整理 React 事件机制、事件绑定、组件构建、组件通信、key、refs、类组件与函数组件、表单和高阶组件。
outline: [2, 3]
---

# React 组件系统

组件是 React 应用的组织单元。一个组件应该有清晰输入、明确输出和可控副作用。组件系统相关主题可以分成三类：组件如何声明，组件如何交互，组件如何复用。

## React 事件机制

React 事件机制以 `SyntheticEvent` 为统一封装。开发者在 JSX 中写的 `onClick`、`onChange`、`onSubmit` 不等同于直接给每个 DOM 节点绑定原生事件，而是进入 React 的事件系统。React 通过统一封装屏蔽浏览器差异，并把事件和更新调度连接起来。

```tsx
function SaveButton() {
  function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault()
    console.log(event.currentTarget.dataset.action)
  }

  return (
    <button data-action="save" onClick={handleClick}>
      保存
    </button>
  )
}
```

`event.target` 表示触发事件的真实目标，`event.currentTarget` 表示当前绑定处理函数的元素。复杂结构中更推荐读取 `currentTarget`，避免误读子元素。

React 17 之前，事件通常委托到 `document`；React 17 起，事件委托移动到根容器。这样多个 React 根节点或多个 React 版本共存时，事件边界更清晰。

### 事件代理

事件代理的思想是：不为每个节点单独注册监听器，而是在上层统一监听，再根据事件冒泡路径分发给对应处理函数。

```tsx
function ActionList() {
  const actions = ['create', 'edit', 'delete']

  function handleClick(event: React.MouseEvent<HTMLUListElement>) {
    const action = (event.target as HTMLElement).dataset.action
    if (action) {
      console.log(`执行动作：${action}`)
    }
  }

  return (
    <ul onClick={handleClick}>
      {actions.map((action) => (
        <li key={action}>
          <button data-action={action}>{action}</button>
        </li>
      ))}
    </ul>
  )
}
```

事件代理减少监听器数量，也方便 React 在事件中批处理状态更新。需要捕获阶段时使用 `onClickCapture`，需要阻止冒泡时调用 `stopPropagation()`。

## React 事件绑定方式

类组件中常见事件绑定方式有三种：constructor 中绑定、class fields 箭头函数、JSX 中临时箭头函数。

```tsx
class SubmitButton extends React.Component {
  constructor(props: {}) {
    super(props)
    this.handleClick = this.handleClick.bind(this)
  }

  handleClick() {
    console.log('submit')
  }

  render() {
    return <button onClick={this.handleClick}>提交</button>
  }
}
```

class fields 写法更简洁：

```tsx
class SubmitButton extends React.Component {
  handleClick = () => {
    console.log('submit')
  }

  render() {
    return <button onClick={this.handleClick}>提交</button>
  }
}
```

JSX 中传箭头函数适合需要附带参数的简单场景：

```tsx
function UserList({ users }: {
  users: Array<{ id: string; name: string }>
}) {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          <button onClick={() => console.log(user.id)}>
            {user.name}
          </button>
        </li>
      ))}
    </ul>
  )
}
```

不要机械地禁止 JSX 箭头函数。真正要关注的是列表很大、子组件被 memo 包裹、回调引用变化导致重复渲染这些场景。必要时用 `useCallback` 或把子项抽成独立组件。

## React 组件构建方式

React 组件构建方式主要有函数组件、类组件和早期的 `React.createClass`。

```tsx
function FunctionPanel({ title }: { title: string }) {
  return <h2>{title}</h2>
}

class ClassPanel extends React.Component<{ title: string }> {
  render() {
    return <h2>{this.props.title}</h2>
  }
}
```

现代项目优先使用函数组件和 Hooks。类组件仍然需要理解，因为错误边界、老项目和部分组件库仍会出现类写法。`React.createClass` 属于历史 API，维护旧代码时需要能读懂。

| 维度 | 函数组件 | 类组件 | `React.createClass` |
| --- | --- | --- | --- |
| 状态 | Hooks | `this.state` | `getInitialState` |
| 生命周期 | effect 和相关 Hook | 生命周期方法 | 旧生命周期 |
| this | 不依赖 | 依赖实例 | 方法自动绑定 |
| 逻辑复用 | 自定义 Hook | HOC、Render props | mixins |
| 当前建议 | 新代码首选 | 维护存量代码 | 只读旧代码 |

## 类组件与函数组件

类组件与函数组件都能根据 props 输出界面，但它们组织状态和副作用的方式不同。

```tsx
function ClockFunction() {
  const [now, setNow] = React.useState(() => new Date())

  React.useEffect(() => {
    const timer = window.setInterval(() => setNow(new Date()), 1000)
    return () => window.clearInterval(timer)
  }, [])

  return <time>{now.toLocaleTimeString()}</time>
}
```

对应的类组件写法：

```tsx
class ClockClass extends React.Component<{}, { now: Date }> {
  state = { now: new Date() }
  private timer: number | undefined

  componentDidMount() {
    this.timer = window.setInterval(() => {
      this.setState({ now: new Date() })
    }, 1000)
  }

  componentWillUnmount() {
    window.clearInterval(this.timer)
  }

  render() {
    return <time>{this.state.now.toLocaleTimeString()}</time>
  }
}
```

函数组件让相关逻辑更容易聚合到一个 Hook 中；类组件把逻辑分散到生命周期方法。迁移时不要逐行翻译，应按数据、订阅、请求、DOM 测量等职责重新拆分。

## React 组件通信

React 组件通信取决于组件关系。

| 关系 | 方案 |
| --- | --- |
| 父子 | props、回调、ref |
| 兄弟 | 状态提升到共同父级 |
| 跨级 | Context、组合插槽 |
| 非嵌套 | 发布订阅、外部 store、URL、缓存层 |
| 多页面共享 | Redux、Zustand、MobX、查询缓存 |

父子通信是基础模式：

```tsx
function Parent() {
  const [keyword, setKeyword] = React.useState('')

  return (
    <SearchInput
      value={keyword}
      onChange={setKeyword}
    />
  )
}

function SearchInput(props: {
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

跨级数据可以用 Context：

```tsx
const ThemeContext = React.createContext<'light' | 'dark'>('light')

function ThemeBadge() {
  const theme = React.useContext(ThemeContext)
  return <span>当前主题：{theme}</span>
}
```

非嵌套组件可以使用发布订阅，但要避免把核心业务状态藏进事件总线。

```ts
type Listener<T> = (payload: T) => void

function createEventBus<T>() {
  const listeners = new Set<Listener<T>>()

  return {
    emit(payload: T) {
      listeners.forEach((listener) => listener(payload))
    },
    subscribe(listener: Listener<T>) {
      listeners.add(listener)
      return () => listeners.delete(listener)
    }
  }
}
```

发布订阅适合通知、埋点、微前端消息等低耦合事件。业务数据如果需要可追踪和可调试，通常放入 store 或共同父级更稳。

## key 的作用

`key` 用于在同层子节点中标识稳定身份。它不是普通 props，不会传进组件内部，而是调和阶段用于判断复用、移动、插入和删除。

```tsx
function TodoList({ todos }: {
  todos: Array<{ id: string; title: string }>
}) {
  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  )
}
```

不要在会插入、删除或排序的列表里使用数组下标作为 key。下标表示位置，不表示业务身份，容易造成输入框内容串行、动画错位或组件局部状态复用错误。

```tsx
// 不推荐：顺序变化时身份不稳定
items.map((item, index) => <Row key={index} item={item} />)

// 推荐：使用业务稳定 id
items.map((item) => <Row key={item.id} item={item} />)
```

key 只在相邻同层元素之间比较。它不能阻止父组件重新渲染，也不是性能优化的万能开关。

## refs 的理解与应用

refs 用来访问 DOM 节点或子组件暴露的命令式能力。React 推荐数据驱动 UI，但聚焦、选中文本、测量尺寸、滚动控制、媒体播放和接入第三方 DOM 库时，ref 很有价值。

```tsx
function AutoFocusInput() {
  const inputRef = React.useRef<HTMLInputElement | null>(null)

  React.useEffect(() => {
    inputRef.current?.focus()
  }, [])

  return <input ref={inputRef} />
}
```

`ref.current` 的变化不会触发重新渲染。如果值变化需要体现在界面上，应使用 state。

### forwardRef 与 useImperativeHandle

普通函数组件不会自动接收 ref。需要转发 ref 时使用 `forwardRef`。

```tsx
const TextInput = React.forwardRef<HTMLInputElement, {
  label: string
}>((props, ref) => {
  return (
    <label>
      {props.label}
      <input ref={ref} />
    </label>
  )
})
```

如果想暴露命令式方法，而不是直接暴露 DOM，可以配合 `useImperativeHandle`。

```tsx
type InputHandle = {
  focus: () => void
  clear: () => void
}

const SmartInput = React.forwardRef<InputHandle>((props, ref) => {
  const inputRef = React.useRef<HTMLInputElement | null>(null)

  React.useImperativeHandle(ref, () => ({
    focus() {
      inputRef.current?.focus()
    },
    clear() {
      if (inputRef.current) {
        inputRef.current.value = ''
      }
    }
  }))

  return <input ref={inputRef} />
})
```

命令式 API 要克制使用。能通过 props 表达的状态，不要改成父组件直接调用子组件方法。

## 受控组件与非受控组件

受控组件的表单值由 React state 控制。非受控组件的值主要保存在 DOM 中，通过 ref 在需要时读取。

```tsx
function ControlledInput() {
  const [name, setName] = React.useState('')

  return (
    <input
      value={name}
      onChange={(event) => setName(event.target.value)}
    />
  )
}
```

```tsx
function UncontrolledInput() {
  const ref = React.useRef<HTMLInputElement | null>(null)

  function handleSubmit() {
    console.log(ref.current?.value)
  }

  return (
    <>
      <input ref={ref} defaultValue="初始值" />
      <button onClick={handleSubmit}>读取</button>
    </>
  )
}
```

受控组件适合实时校验、联动、格式化、禁用提交和表单状态汇总。非受控组件适合文件输入、一次性读取、接入非 React 表单库和简单表单。不要在同一个输入上同时用 `value` 与 `defaultValue` 表达同一份状态。

## 高阶组件

高阶组件是接收组件并返回新组件的函数。它适合封装权限、埋点、主题、数据注入、错误兜底等横切能力。

```tsx
function withPermission<P>(
  Component: React.ComponentType<P>,
  permission: string
) {
  return function PermissionWrapper(props: P) {
    const allowed = usePermission(permission)

    if (!allowed) {
      return <span>无权限</span>
    }

    return <Component {...props} />
  }
}
```

高阶组件的优点是复用边界清晰，缺点是容易形成包装层嵌套，props 来源不够直观，并且 ref、静态属性和 displayName 需要额外处理。

```tsx
function withLoading<P>(Component: React.ComponentType<P>) {
  function LoadingWrapper(props: P & { loading: boolean }) {
    if (props.loading) {
      return <span>加载中...</span>
    }

    return <Component {...props} />
  }

  LoadingWrapper.displayName = `withLoading(${Component.displayName ?? Component.name})`
  return LoadingWrapper
}
```

Hooks 出现后，很多逻辑复用可以改成自定义 Hook。但 HOC 在路由守卫、错误边界适配、权限包装和组件库增强中仍然有位置。

## Render props

Render props 把可复用逻辑封装在组件中，再通过函数把状态交给调用方决定如何渲染。

```tsx
function MouseTracker(props: {
  children: (point: { x: number; y: number }) => React.ReactNode
}) {
  const [point, setPoint] = React.useState({ x: 0, y: 0 })

  return (
    <div onMouseMove={(event) => {
      setPoint({ x: event.clientX, y: event.clientY })
    }}>
      {props.children(point)}
    </div>
  )
}
```

Render props 比 HOC 更直观看到数据来源，但嵌套较多时可读性下降。现代项目常把同类逻辑改成自定义 Hook。

## 组件系统检查清单

| 主题 | 建议 |
| --- | --- |
| 事件 | 使用函数引用，理解 SyntheticEvent 和事件代理 |
| 绑定 | 类组件处理 this，函数组件关注回调引用稳定性 |
| 通信 | 优先 props 和状态提升，跨级低频数据用 Context |
| key | 使用稳定业务 id，不用易变化下标 |
| refs | 只处理命令式需求，不保存业务状态 |
| 表单 | 需要联动校验时用受控组件，简单读取可用非受控 |
| HOC | 处理 displayName、ref 透传、props 透传和静态属性 |
| Render props | 适合显式暴露内部状态，复杂逻辑优先考虑 Hook |

