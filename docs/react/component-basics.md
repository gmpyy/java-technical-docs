---
title: React 组件基础
description: 系统整理 React 组件、事件、refs、Context、Portals、受控组件、组件声明方式和基础性能策略。
outline: [2, 3]
---

# React 组件基础

React 应用由组件构成。组件可以是函数，也可以是类；组件执行后得到 React Element；React 再根据这些元素描述创建或更新真实界面。理解组件基础，需要把“事件、数据入口、组件声明方式、refs、Context、组合模式和渲染边界”放在一起看。

## React 事件机制

React 的事件系统以 SyntheticEvent 为统一封装。开发者写在 JSX 上的 `onClick`、`onChange`、`onSubmit` 并不是直接等同于浏览器原生事件监听，而是进入 React 自己的事件分发体系。SyntheticEvent 屏蔽了不同浏览器的差异，提供接近 W3C 标准的事件接口，例如 `preventDefault`、`stopPropagation`、`target`、`currentTarget`。

```tsx
function SaveButton() {
  function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault()
    console.log(event.target)
    console.log(event.currentTarget)
  }

  return <button onClick={handleClick}>保存</button>
}
```

React 事件和普通 HTML 事件的主要区别有三点：

| 对比点 | React 事件 | 普通 HTML 事件 |
| --- | --- | --- |
| 命名 | 驼峰形式，如 `onClick` | 小写形式，如 `onclick` |
| 处理函数 | 传入函数引用 | 可以是字符串或函数 |
| 分发方式 | 通过 React 事件系统统一派发 | 直接绑定到 DOM 节点或通过浏览器冒泡 |

React 17 之前，事件通常委托到 `document`；React 17 起，事件委托位置移动到应用根容器，这样多个 React 版本或多个根节点共存时，事件边界更清晰。

## 事件代理

React 组件中事件代理的基本思想是：不把每个监听器都直接绑定在目标 DOM 上，而是把监听集中到根容器，再根据事件冒泡路径找到对应组件的处理函数。这样能减少监听器数量，也能配合 React Fiber 树完成优先级调度和更新批处理。

```tsx
function Menu() {
  const items = ['新建', '打开', '保存']

  function handleClick(event: React.MouseEvent<HTMLUListElement>) {
    const action = (event.target as HTMLElement).dataset.action
    if (action) {
      console.log(`执行：${action}`)
    }
  }

  return (
    <ul onClick={handleClick}>
      {items.map((item) => (
        <li key={item}>
          <button data-action={item}>{item}</button>
        </li>
      ))}
    </ul>
  )
}
```

需要注意，React 的事件对象仍然保留冒泡和捕获模型。想监听捕获阶段，可以使用 `onClickCapture`。想阻止冒泡，可以调用 `event.stopPropagation()`，但这只应该用在明确需要隔离事件的地方。

## Component、Element、Instance

React Component、React Element 和组件实例经常被混在一起，它们实际代表三个层面。

| 名称 | 含义 | 示例 |
| --- | --- | --- |
| React Component | 组件定义，可以是函数或 class | `function UserCard() {}` |
| React Element | 调用组件或 JSX 后得到的普通对象描述 | `<UserCard />` |
| Instance | 类组件运行时实例，函数组件没有传统实例 | `this.setState()` 所在的对象 |

```tsx
function UserCard() {
  return <div>用户卡片</div>
}

const element = <UserCard />
```

在这段代码中，`UserCard` 是组件定义，`element` 是 React Element。React Element 本质上是一个不可变的描述对象，里面记录了类型、props、key 等信息。React 根据这些描述对象构建 Fiber 节点，再决定如何更新界面。

## 组件声明方式

React 声明组件有三类历史方式：函数组件、类组件、`React.createClass`。现代项目优先使用函数组件和 Hooks；类组件仍然需要读懂，因为很多老项目和第三方组件库仍有 class 写法；`React.createClass` 属于旧 API，只在维护历史代码时会遇到。

```tsx
function FunctionPanel(props: { title: string }) {
  return <h2>{props.title}</h2>
}

class ClassPanel extends React.Component<{ title: string }> {
  render() {
    return <h2>{this.props.title}</h2>
  }
}
```

`React.createClass` 和 `extends Component` 的差异主要包括：

| 维度 | `React.createClass` | `extends Component` |
| --- | --- | --- |
| 语法基础 | React 早期工厂 API | ES class |
| 默认 props | 使用 `getDefaultProps` | 使用 `static defaultProps` 或参数默认值 |
| 初始状态 | 使用 `getInitialState` | 在 constructor 或类字段中初始化 |
| 方法 this | 自动绑定 | 需要手动绑定、使用箭头函数或 class fields |
| 当前建议 | 只读旧代码 | 维护 class 组件时使用 |

## 函数组件与类组件

函数组件和类组件都能接收 props 并返回界面描述。差异在于状态、生命周期和实例模型。

| 维度 | 函数组件 | 类组件 |
| --- | --- | --- |
| 状态 | 通过 `useState`、`useReducer` 等 Hook | 通过 `this.state` 和 `this.setState` |
| 生命周期 | 通过 `useEffect` 等 Hook 表达副作用 | 通过生命周期方法表达 |
| this | 不需要 | 依赖实例和 `this` |
| 逻辑复用 | 自定义 Hook | HOC、Render props、继承较少使用 |
| 当前趋势 | 新代码首选 | 维护旧代码仍常见 |

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

类组件不是“过时知识”，而是 React 历史和许多存量项目的重要组成。理解 class 生命周期也有助于理解 Hooks 与渲染提交阶段的关系。

## 有状态组件与无状态组件

有状态组件维护自己的数据变化，无状态组件只根据 props 渲染 UI。现代项目中，这个区分不再等同于 class 与 function，因为函数组件也可以通过 Hooks 拥有状态。

```tsx
function PriceView({ amount }: { amount: number }) {
  return <strong>¥{amount.toFixed(2)}</strong>
}

function CartPanel() {
  const [amount, setAmount] = React.useState(99)

  return (
    <>
      <PriceView amount={amount} />
      <button onClick={() => setAmount(amount + 10)}>加价</button>
    </>
  )
}
```

实践中，可以把业务流程和数据请求放在容器型组件，把纯展示逻辑放在展示型组件。这样测试、复用和样式调整都会更轻松。

## 高阶组件、Render props 与 React Hooks

高阶组件、Render props 和 React Hooks 都是复用逻辑的方案。它们不断演进，是因为 React 应用越来越需要在多个组件间共享状态逻辑、副作用逻辑和订阅逻辑。

### 高阶组件

高阶组件是接收组件并返回新组件的函数。它常用于权限、埋点、数据注入、主题注入等横切逻辑。

```tsx
function withLoading<P>(Component: React.ComponentType<P>) {
  return function LoadingWrapper(props: P & { loading: boolean }) {
    if (props.loading) {
      return <span>加载中...</span>
    }

    return <Component {...props} />
  }
}
```

高阶组件的优点是复用方式清晰，缺点是容易形成包装层嵌套，props 来源不够直观，并且静态属性、ref 透传需要额外处理。

### Render props

Render props 把可复用逻辑封装在一个组件中，再通过函数把内部状态交给调用方决定如何渲染。

```tsx
function MouseTracker(props: {
  children: (point: { x: number; y: number }) => React.ReactNode
}) {
  const [point, setPoint] = React.useState({ x: 0, y: 0 })

  return (
    <div onMouseMove={(event) => setPoint({ x: event.clientX, y: event.clientY })}>
      {props.children(point)}
    </div>
  )
}
```

Render props 解决了 HOC 中 props 来源不透明的问题，但会增加嵌套层级，复杂页面中可读性也会下降。

### React Hooks

React Hooks 允许函数组件在不引入 class 的情况下使用状态和副作用，也让逻辑复用变成普通函数组合。

```tsx
function useOnlineStatus() {
  const [online, setOnline] = React.useState(navigator.onLine)

  React.useEffect(() => {
    const handleOnline = () => setOnline(true)
    const handleOffline = () => setOnline(false)

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  return online
}
```

Hooks 的核心优势是组合自然、类型友好、没有包装地狱。代价是必须理解闭包、依赖数组和 Hook 调用顺序。

## React.Component 与 React.PureComponent

`React.Component` 默认每次父组件更新或自身状态更新时都会进入渲染流程。`React.PureComponent` 内置了浅比较，相当于默认实现了 `shouldComponentUpdate`：当 props 和 state 的浅层引用没有变化时，可以跳过本次重新渲染。

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

`PureComponent` 的关键限制是浅比较。如果直接修改对象或数组，引用不变，React 可能误以为没有变化。

```tsx
// 不推荐：原数组引用没有改变
items.push(nextItem)
this.setState({ items })

// 推荐：创建新数组引用
this.setState({ items: [...items, nextItem] })
```

函数组件中与它相似的是 `React.memo`。不过无论使用 `PureComponent` 还是 `React.memo`，都应该先确认渲染确实昂贵，否则比较成本可能大于收益。

## 触发重新渲染的方式

常见触发重新渲染的情况包括：

| 场景 | 说明 |
| --- | --- |
| state 更新 | 类组件调用 `setState`，函数组件调用状态 setter |
| props 更新 | 父组件重新渲染并传入新的 props |
| Context 更新 | 组件读取的 Context value 发生变化 |
| forceUpdate | 类组件显式跳过状态比较，强制进入渲染 |

重新渲染时，`render` 或函数组件会再次执行，得到新的 React Element 树。React 不会简单地把整棵真实 DOM 删除重建，而是进入调和过程，比较新旧元素，计算最小必要变更。

```tsx
function Parent() {
  const [count, setCount] = React.useState(0)

  console.log('Parent render')

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

即使子组件 props 看起来没变，父组件重新执行时子组件也可能重新执行。是否跳过需要依靠 `React.memo`、`PureComponent` 或更合理的组件拆分。

## 判断是否重新渲染

React 判断组件是否需要更新，主要看更新是否进入了这条组件路径，以及是否有明确的跳过条件。类组件可以通过 `shouldComponentUpdate` 控制；函数组件可以使用 `React.memo` 让 React 对 props 做浅比较。

```tsx
const UserName = React.memo(function UserName(props: { name: string }) {
  return <span>{props.name}</span>
})

class Score extends React.Component<{ value: number }> {
  shouldComponentUpdate(nextProps: { value: number }) {
    return nextProps.value !== this.props.value
  }

  render() {
    return <strong>{this.props.value}</strong>
  }
}
```

避免不必要 render 的常见策略包括：把状态下沉到真正需要它的组件、拆分大组件、保持 props 引用稳定、使用 `useMemo` 和 `useCallback` 缓存昂贵计算或回调、合理使用列表 `key`、避免在 render 中创建巨大的临时对象。

## Fragment

React 组件必须返回一个根节点。Fragment 允许返回多个兄弟节点而不额外创建真实 DOM，适合表格行、列表片段和布局中不希望多一层包裹的场景。

```tsx
function UserFields() {
  return (
    <>
      <dt>姓名</dt>
      <dd>小林</dd>
    </>
  )
}
```

如果需要给 Fragment 加 `key`，必须使用完整写法：

```tsx
function TermList({ items }: { items: string[] }) {
  return (
    <dl>
      {items.map((item) => (
        <React.Fragment key={item}>
          <dt>{item}</dt>
          <dd>{item.length}</dd>
        </React.Fragment>
      ))}
    </dl>
  )
}
```

## refs 与 DOM 元素

React 推荐通过数据驱动 UI，但某些场景仍需要直接访问 DOM，例如聚焦输入框、测量尺寸、控制滚动位置、接入第三方 DOM 库或播放媒体。函数组件使用 `useRef`，类组件使用 `createRef`。

```tsx
function AutoFocusInput() {
  const inputRef = React.useRef<HTMLInputElement | null>(null)

  React.useEffect(() => {
    inputRef.current?.focus()
  }, [])

  return <input ref={inputRef} />
}
```

不要在 render 阶段依赖 refs 读取 DOM。render 阶段应该是纯计算，真实 DOM 还没有保证完成提交；refs 的可靠读取位置通常是 `useEffect`、`useLayoutEffect`、`componentDidMount`、`componentDidUpdate` 或事件回调。

refs 的典型应用场景有：

| 场景 | 用法 |
| --- | --- |
| 表单聚焦 | `inputRef.current?.focus()` |
| 媒体控制 | 调用 `video.play()`、`pause()` |
| 尺寸测量 | 在 `useLayoutEffect` 中读取 `getBoundingClientRect()` |
| 第三方库 | 把 DOM 容器交给图表或编辑器 |
| 暴露子组件命令 | 配合 `forwardRef` 与 `useImperativeHandle` |

## forwardRef

`React.forwardRef` 用于把父组件传入的 ref 转发到子组件内部的 DOM 或命令对象。普通函数组件不会自动接收 ref，因为 ref 不是普通 props。

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

function Form() {
  const ref = React.useRef<HTMLInputElement | null>(null)

  return (
    <>
      <TextInput ref={ref} label="用户名" />
      <button onClick={() => ref.current?.focus()}>聚焦</button>
    </>
  )
}
```

组件库中，`forwardRef` 很常见，因为调用方经常需要聚焦、测量或接入表单库。

## Portals

Portals 允许把子节点渲染到父组件 DOM 层级之外的位置，但事件仍按 React 组件树冒泡。它适合弹窗、提示框、下拉层、全局通知等需要脱离局部 `overflow` 或 `z-index` 限制的场景。

```tsx
import { createPortal } from 'react-dom'

function Dialog(props: { open: boolean; onClose: () => void }) {
  if (!props.open) {
    return null
  }

  return createPortal(
    <div role="dialog" aria-modal="true">
      <p>确认提交当前内容？</p>
      <button onClick={props.onClose}>关闭</button>
    </div>,
    document.body
  )
}
```

使用 Portals 时，要额外处理焦点管理、滚动锁定、键盘关闭、无障碍属性和卸载清理。

## Context

Context 用于跨层级传递数据，典型场景是主题、语言、登录用户、权限、配置项。它解决的是 props 层层透传带来的样板代码。

```tsx
const ThemeContext = React.createContext<'light' | 'dark'>('light')

function ThemeBadge() {
  const theme = React.useContext(ThemeContext)
  return <span>当前主题：{theme}</span>
}

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <ThemeBadge />
    </ThemeContext.Provider>
  )
}
```

React 并不推荐优先把所有共享数据都放入 Context，原因有三点：

| 风险 | 说明 |
| --- | --- |
| 复用性下降 | 组件隐式依赖外部上下文，单独复用时需要包 Provider |
| 更新影响面变大 | Provider value 变化会影响读取该 Context 的后代 |
| 数据来源不直观 | props 能直接看到依赖，Context 容易隐藏依赖 |

Context 更适合低频变化的全局数据。高频业务状态可以结合状态管理库、状态下沉或局部 store 处理。

## 受控组件与非受控组件

受控组件的表单值由 React state 控制，非受控组件的表单值主要保存在 DOM 中，通过 ref 在需要时读取。

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
      <input ref={ref} defaultValue="默认值" />
      <button onClick={handleSubmit}>读取</button>
    </>
  )
}
```

受控组件适合需要实时校验、联动、格式化和提交前汇总的表单。非受控组件适合简单表单、文件输入和接入非 React 表单库。不要在同一个输入上混用 `value` 与 `defaultValue` 来表达同一个状态。

## this 绑定与构造函数

类组件中，事件处理函数作为回调传递时会丢失 `this`。常见解决方式有三种：在 constructor 中绑定、使用 class fields 箭头函数、在 JSX 中传入箭头函数。

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

构造函数并不是类组件必须具备的。只有在初始化 state、绑定方法、创建实例字段时才需要 constructor。使用 constructor 时必须先调用 `super(props)`，否则无法访问 `this`。

```tsx
class Counter extends React.Component<{}, { count: number }> {
  state = {
    count: 0
  }

  handleClick = () => {
    this.setState((state) => ({ count: state.count + 1 }))
  }

  render() {
    return <button onClick={this.handleClick}>{this.state.count}</button>
  }
}
```

## React-Intl

React-Intl 是国际化方案之一，核心思路是把文案、数字、日期、货币等格式化能力封装为组件或 Hook，并通过 Provider 注入当前语言环境和消息字典。

```tsx
import { IntlProvider, FormattedMessage } from 'react-intl'

const messages = {
  hello: '你好，{name}'
}

function App() {
  return (
    <IntlProvider locale="zh-CN" messages={messages}>
      <FormattedMessage id="hello" values={{ name: 'React' }} />
    </IntlProvider>
  )
}
```

它的工作原理可以分为三层：最外层 Provider 提供 locale 和 messages；组件或 Hook 按 id 读取消息模板；格式化器根据语言环境输出最终文本。大型项目通常还会配合按语言拆包、缺失文案检查和构建期提取。

## 组件基础实践清单

| 主题 | 建议 |
| --- | --- |
| 事件 | 使用函数引用，避免在复杂列表中制造大量无意义闭包 |
| refs | 只在命令式需求中使用，避免用 ref 存业务状态 |
| Context | 适合主题、语言、用户等跨层级低频数据 |
| Portals | 弹窗类组件要处理焦点、滚动、键盘和卸载 |
| HOC | 注意 displayName、ref 透传、静态属性复制 |
| Render props | 避免过深嵌套，复杂逻辑优先考虑 Hook |
| 受控表单 | 适合校验、联动、提交前汇总 |
| 非受控表单 | 适合文件输入和简单读取 |

