---
title: React 工程实践
description: 整理 React 命名、版本演进、全局弹窗、持久化、TypeScript、JSX、SSR、严格模式、React.Children 与设计模式。
outline: [2, 3]
---

# React 工程实践

React 工程实践关注的是如何把组件模型落到真实项目：命名是否清晰，弹窗和路由如何组织，数据如何持久化，TypeScript 如何接入，SSR 如何理解，严格模式如何帮助发现问题，以及组件抽象背后的设计模式。这里整理的是常见开发场景中的可执行原则。

## 组件命名

React 组件命名推荐使用大驼峰形式，也就是 PascalCase，例如 `UserCard`、`OrderTable`、`RouteGuard`。小写标签会被 React 当作宿主元素，例如 `div`、`span`、`button`。

```tsx
function UserCard() {
  return <article>用户信息</article>
}

function App() {
  return <UserCard />
}
```

文件命名可以根据团队规范选择 `UserCard.tsx` 或 `user-card.tsx`，但组件导出名建议保持 PascalCase。自定义 Hook 必须以 `use` 开头，例如 `useAuth`、`useDebounce`，这样 React 规则检查工具才能识别它。

## 版本演进关注点

React 版本演进通常围绕并发渲染、服务端渲染、编译优化、开发者工具和副作用模型展开。以当前主线 React 19.2 为例，值得关注的方向包括 `<Activity />`、`useEffectEvent`、服务端渲染恢复能力、性能轨道和 React Server Components 相关修复。

版本升级时不要只看“新增 API”，还要看这些问题：

| 检查项 | 说明 |
| --- | --- |
| React 与 React DOM 是否同版本 | 避免运行时能力不匹配 |
| 框架兼容性 | Next.js、Remix、Vite 插件、测试库是否支持 |
| 严格模式行为 | 开发环境可能暴露重复执行或清理问题 |
| 服务端能力 | SSR、RSC、流式渲染是否涉及安全补丁 |
| 第三方库 | 组件库、状态库、路由库是否声明兼容 |

```json
{
  "dependencies": {
    "react": "19.2.1",
    "react-dom": "19.2.1"
  }
}
```

生产项目升级前应创建独立分支，运行单元测试、端到端流程、构建检查和关键页面回归。涉及服务端组件或框架集成时，还要关注安全公告和框架补丁版本。

## 全局 Dialog 实现

全局 dialog 通常由三部分组成：状态管理入口、Portal 渲染层、命令式或声明式调用 API。最简单的方案是用 Context 暴露 `open` 和 `close` 方法，再把弹窗通过 Portal 挂到 `document.body`。

```tsx
type DialogOptions = {
  title: string
  content: React.ReactNode
}

const DialogContext = React.createContext<{
  open: (options: DialogOptions) => void
  close: () => void
} | null>(null)

function DialogProvider({ children }: { children: React.ReactNode }) {
  const [dialog, setDialog] = React.useState<DialogOptions | null>(null)

  const api = React.useMemo(() => ({
    open: setDialog,
    close: () => setDialog(null)
  }), [])

  return (
    <DialogContext.Provider value={api}>
      {children}
      {dialog ? (
        <GlobalDialog
          title={dialog.title}
          onClose={api.close}
        >
          {dialog.content}
        </GlobalDialog>
      ) : null}
    </DialogContext.Provider>
  )
}
```

```tsx
function GlobalDialog(props: {
  title: string
  children: React.ReactNode
  onClose: () => void
}) {
  return createPortal(
    <div role="dialog" aria-modal="true">
      <h2>{props.title}</h2>
      {props.children}
      <button onClick={props.onClose}>关闭</button>
    </div>,
    document.body
  )
}
```

全局弹窗要注意焦点陷阱、Esc 关闭、遮罩点击、滚动锁定、层级管理和多个弹窗队列。复杂组件库通常还会把 confirm 返回 Promise，便于业务流程串联。

## 数据持久化

React 数据持久化可以发生在多个层次：浏览器存储、URL、服务端、状态管理中间件或查询缓存。选择哪种方式取决于数据生命周期和安全性。

| 数据类型 | 建议位置 |
| --- | --- |
| 登录 token | 优先 HttpOnly Cookie；若放 localStorage 要评估 XSS 风险 |
| 主题、语言 | localStorage 或 cookie |
| 搜索条件 | URL query，方便分享和刷新恢复 |
| 表单草稿 | localStorage、IndexedDB 或服务端草稿 |
| 服务端列表缓存 | 查询缓存库或框架数据层 |

```tsx
function usePersistentState(key: string, initialValue: string) {
  const [value, setValue] = React.useState(() => {
    return window.localStorage.getItem(key) ?? initialValue
  })

  React.useEffect(() => {
    window.localStorage.setItem(key, value)
  }, [key, value])

  return [value, setValue] as const
}
```

页面重新加载时保留数据，通常靠 URL、localStorage、sessionStorage、IndexedDB、Cookie 或服务端重新拉取。不要把敏感数据随意放到可被脚本读取的位置。

## React 与 Vue 的理解

React 和 Vue 都是组件化 UI 方案，都把界面拆成组件，都关注状态到视图的映射。主要差异在于设计取向。

| 维度 | React | Vue |
| --- | --- | --- |
| UI 描述 | JSX，JavaScript 表达能力强 | 模板为主，约束更明确 |
| 数据变化 | setState/Hook 触发渲染 | 响应式依赖追踪 |
| 逻辑复用 | Hooks、组件组合 | Composition API、组合式函数 |
| 性能模型 | Fiber、调和、memo 优化 | 响应式依赖 + 编译优化 |
| 学习曲线 | JS 能力要求更高 | 模板上手更快 |

React 更像一个 UI 运行时和组件模型，需要团队自行组合路由、状态、请求、样式等方案。Vue 提供更完整的官方生态体验。选择时应看团队经验、项目复杂度和生态要求。

## TypeScript 写 React

React 可以很好地使用 TypeScript。常见文件后缀是 `.tsx`，props、state、事件、ref 和泛型组件都可以获得类型检查。

```tsx
type UserCardProps = {
  id: string
  name: string
  onSelect?: (id: string) => void
}

function UserCard({ id, name, onSelect }: UserCardProps) {
  return (
    <button onClick={() => onSelect?.(id)}>
      {name}
    </button>
  )
}
```

事件类型可以从 React 命名空间读取。

```tsx
function NameInput() {
  const [name, setName] = React.useState('')

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    setName(event.target.value)
  }

  return <input value={name} onChange={handleChange} />
}
```

ref 类型需要写出目标 DOM 类型。

```tsx
function FocusInput() {
  const ref = React.useRef<HTMLInputElement | null>(null)

  return (
    <>
      <input ref={ref} />
      <button onClick={() => ref.current?.focus()}>聚焦</button>
    </>
  )
}
```

TypeScript 的价值不只是补全，还包括让组件边界、回调签名和状态结构更稳定。

## React 设计思路

React 的设计理念可以概括为五点：

1. 声明式 UI：开发者描述目标界面，React 负责更新细节。
2. 组件化：把界面和逻辑拆成可组合单元。
3. 单向数据流：数据从父到子，变化通过明确入口发生。
4. 纯渲染：render 尽量保持纯计算，副作用放到提交后。
5. 运行时调度：通过 Fiber 和优先级让复杂 UI 更可控。

```tsx
function UserPage({ user }: {
  user: { name: string; locked: boolean }
}) {
  return (
    <section>
      <h1>{user.name}</h1>
      {user.locked ? <LockTip /> : <ProfileForm user={user} />}
    </section>
  )
}
```

这段代码没有直接操作 DOM，也没有描述从旧界面怎么变成新界面，只描述“当前状态应该是什么样”。

## props.children 与 React.Children

`props.children` 是组件接收到的子节点，可能是单个元素、字符串、数组、null 或其他可渲染值。`React.Children` 是一组处理 children 的工具方法，可以安全遍历、计数、转换。

```tsx
function Card({ children }: { children: React.ReactNode }) {
  return <section className="card">{children}</section>
}
```

`React.Children.map` 和 JavaScript 数组的 `map` 不完全相同。children 不一定是数组，`React.Children.map` 能处理单个 child、空值和嵌套结构，并保持 key 处理更符合 React 规则。

```tsx
function Stack({ children }: { children: React.ReactNode }) {
  return (
    <div className="stack">
      {React.Children.map(children, (child, index) => (
        <div className="stack-item" data-index={index}>
          {child}
        </div>
      ))}
    </div>
  )
}
```

如果需要断言只有一个子元素，可以使用 `React.Children.only(children)`。这常见于触发器组件、动画组件和需要克隆子元素的组件。

## 状态提升

状态提升是把多个组件共享的状态移动到它们最近的共同父组件中，再通过 props 分发。它适合兄弟组件联动、表单拆分、筛选条件和结果列表联动等场景。

```tsx
function TemperatureCalculator() {
  const [celsius, setCelsius] = React.useState('')

  return (
    <>
      <TemperatureInput value={celsius} onChange={setCelsius} />
      <BoilingVerdict celsius={Number(celsius)} />
    </>
  )
}
```

状态提升不是把所有状态都放到页面顶层。只提升真正需要共享的状态，局部交互状态仍应留在局部组件中。

## constructor 与 getInitialState

`getInitialState` 来自 `React.createClass`，用于返回初始 state。`constructor` 是 ES class 初始化入口，用于 class 组件初始化 state、绑定方法或创建实例字段。

```tsx
class LegacyEquivalent extends React.Component<{}, { count: number }> {
  constructor(props: {}) {
    super(props)
    this.state = {
      count: 0
    }
  }

  render() {
    return <span>{this.state.count}</span>
  }
}
```

现代 class 组件可以使用类字段初始化 state，函数组件则用 `useState`。维护历史代码时，看到 `getInitialState` 就把它理解为旧写法中的初始状态函数。

## 严格模式

React 严格模式通过 `<React.StrictMode>` 开启，只在开发环境执行额外检查，不会影响生产构建行为。它能帮助发现不安全生命周期、意外副作用、旧字符串 ref、废弃 API 和清理函数缺失等问题。

```tsx
import { createRoot } from 'react-dom/client'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

开发环境中，严格模式可能让某些函数或 effect 执行两次，用来暴露副作用不纯和清理不完整的问题。不要简单把它当成 bug；应该检查 effect 是否正确清理、render 是否保持纯函数。

## 遍历渲染

React 中遍历列表最常见的是数组 `map`。渲染列表时必须提供稳定 key。

```tsx
function TagList({ tags }: { tags: string[] }) {
  return (
    <ul>
      {tags.map((tag) => (
        <li key={tag}>{tag}</li>
      ))}
    </ul>
  )
}
```

对象数据可以先转成数组再渲染。

```tsx
function ScoreTable({ scores }: {
  scores: Record<string, number>
}) {
  return (
    <dl>
      {Object.entries(scores).map(([name, score]) => (
        <React.Fragment key={name}>
          <dt>{name}</dt>
          <dd>{score}</dd>
        </React.Fragment>
      ))}
    </dl>
  )
}
```

避免在渲染中对超大数据做复杂计算。大列表应考虑分页、虚拟列表或预计算。

## 页面刷新后保留数据

页面重新加载会清空内存中的 React state。保留数据有几种方式：

| 方式 | 适合数据 |
| --- | --- |
| URL 参数 | 筛选条件、分页、tab |
| localStorage | 主题、草稿、非敏感配置 |
| sessionStorage | 当前会话临时状态 |
| Cookie | 登录态、服务端可读偏好 |
| IndexedDB | 大量结构化离线数据 |
| 服务端 | 用户资料、订单、权限等权威数据 |

```tsx
function useQueryKeyword() {
  const [params, setParams] = useSearchParams()

  const keyword = params.get('keyword') ?? ''

  const setKeyword = (nextKeyword: string) => {
    setParams((prev) => {
      prev.set('keyword', nextKeyword)
      return prev
    })
  }

  return [keyword, setKeyword] as const
}
```

能放进 URL 的状态优先放 URL，因为它天然支持刷新恢复、分享和浏览器前进后退。

## react.js、react-dom.js 与 babel.js

在传统浏览器直引模式中，这三个库职责不同：

| 文件 | 作用 |
| --- | --- |
| `react.js` | 提供 React 核心能力，如组件、Element、Hooks |
| `react-dom.js` | 提供把 React 渲染到 DOM 的能力 |
| `babel.js` | 在浏览器中把 JSX 或新语法转换成可执行 JavaScript |

```html
<div id="root"></div>
<script type="text/babel">
  function App() {
    return <h1>Hello React</h1>
  }

  ReactDOM.createRoot(document.getElementById('root')).render(<App />)
</script>
```

现代工程通常不在生产环境使用浏览器端 Babel，而是通过 Vite、Webpack、Rspack 等构建工具在构建阶段转换 JSX 和 TypeScript。

## JSX 是否必须

React 不强制使用 JSX。JSX 只是 `React.createElement` 或新版 JSX runtime 的语法糖。理论上可以手写创建调用，但可读性会明显下降。

```tsx
const jsxElement = <h1 className="title">Hello</h1>
```

等价思想类似：

```ts
const rawElement = React.createElement(
  'h1',
  { className: 'title' },
  'Hello'
)
```

使用 JSX 的价值是结构接近最终 UI，组件嵌套清晰，表达条件渲染和列表渲染更自然。

## 为什么以前写 JSX 需要引入 React

旧 JSX 转换会把 JSX 编译为 `React.createElement(...)`，所以文件中即使没有直接使用 `React` 变量，也必须引入它。

```tsx
import React from 'react'

function App() {
  return <h1>Hello</h1>
}
```

新 JSX runtime 会从 `react/jsx-runtime` 自动引入需要的创建函数，因此很多现代项目不再要求每个 JSX 文件都写 `import React from 'react'`。

```tsx
function App() {
  return <h1>Hello</h1>
}
```

维护旧项目时，是否必须引入 React 取决于构建配置和 React 版本。

## async/await

React 事件处理函数和 effect 内部都可以使用 async/await，但 effect 回调本身不应该直接声明为 async，因为 async 函数返回 Promise，而 effect 期望返回清理函数或 undefined。

```tsx
function UserPanel({ id }: { id: string }) {
  const [user, setUser] = React.useState<{ name: string } | null>(null)

  React.useEffect(() => {
    let active = true

    async function load() {
      const nextUser = await fetchUser(id)
      if (active) {
        setUser(nextUser)
      }
    }

    load()

    return () => {
      active = false
    }
  }, [id])

  return <div>{user?.name}</div>
}
```

事件处理函数可以直接写 async。

```tsx
async function handleSubmit() {
  await saveForm()
  toast('保存成功')
}
```

需要处理错误、取消和过期响应，不要只写 happy path。

## SSR

React SSR 是服务端渲染。服务端先把 React 组件渲染成 HTML 字符串或流，浏览器拿到 HTML 后可以更快展示首屏；随后客户端加载 JavaScript，进行 hydration，把静态 HTML 绑定成可交互应用。

```tsx
import { renderToPipeableStream } from 'react-dom/server'

function handleRequest(res: {
  setHeader: (name: string, value: string) => void
}) {
  const stream = renderToPipeableStream(<App />, {
    onShellReady() {
      res.setHeader('content-type', 'text/html')
    }
  })

  return stream
}
```

SSR 的优势包括首屏内容更快、SEO 更友好、可以流式传输。代价是服务端复杂度上升，需要处理数据预取、缓存、同构差异、hydration 不一致、部署成本和安全边界。

## 为什么 React 使用 JSX

JSX 把 UI 结构和相关逻辑放在同一个 JavaScript 表达式中。它不是模板字符串，而是可被编译的语法扩展。React 使用 JSX 的原因包括：

| 原因 | 说明 |
| --- | --- |
| 结构直观 | 嵌套关系接近最终 UI |
| 表达能力强 | 可以直接使用变量、函数、条件和数组 |
| 类型友好 | TypeScript 能检查 props |
| 工具链成熟 | 编译、lint、格式化和编辑器支持完善 |
| 组件组合自然 | 自定义组件和原生元素写法一致 |

```tsx
function Status({ loading, error }: {
  loading: boolean
  error?: string
}) {
  return (
    <section>
      {loading ? <p>加载中</p> : null}
      {error ? <p role="alert">{error}</p> : null}
    </section>
  )
}
```

JSX 的本质仍然是 JavaScript。花括号内写的是表达式，不是任意语句。

## 高阶组件的设计模式

React 中的高阶组件体现了装饰器模式和函数组合思想。它不修改原组件，而是返回一个增强后的新组件，把横切能力包在外层。

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

使用高阶组件时要注意：

| 注意点 | 说明 |
| --- | --- |
| 不在 render 中创建 HOC | 会导致每次渲染产生新组件类型 |
| 设置 displayName | 方便调试组件树 |
| 透传无关 props | 保持包装前后的调用体验 |
| 处理 ref | 需要 `forwardRef` |
| 复制静态属性 | 组件库场景可能需要 hoist |

Hooks 出现后，许多逻辑复用场景可以改用自定义 Hook；但权限、布局包装、错误边界适配等场景仍然可能使用 HOC。

## 工程实践检查清单

| 主题 | 建议 |
| --- | --- |
| 命名 | 组件 PascalCase，Hook 以 `use` 开头 |
| 版本 | 升级时同时检查 React、React DOM、框架和组件库 |
| Dialog | 使用 Portal，并处理焦点、滚动、键盘和层级 |
| 持久化 | URL 优先表达可分享状态，敏感数据谨慎存储 |
| TypeScript | props、事件、ref、状态都写清类型 |
| JSX | 理解它是语法糖，不是运行时魔法 |
| SSR | 同时评估首屏收益、缓存策略和 hydration 成本 |
| 严格模式 | 把重复执行当作副作用检查信号 |
| React.Children | 用于安全处理不确定 children 结构 |

