---
title: React 工程实践
description: 整理 React 错误捕获、服务端渲染、数据持久化、严格模式、React.Children 和常见问题解决方式。
outline: [2, 3]
---

# React 工程实践

React 工程实践关注的是如何把组件模型落到真实项目中：错误如何兜底，服务端渲染如何工作，页面刷新后数据如何保留，严格模式暴露的问题如何理解，children 如何处理，以及常见项目问题如何定位。

## React 错误捕获

React 错误捕获主要依赖 Error Boundary。错误边界可以捕获子组件渲染、生命周期和 constructor 中抛出的错误，并展示降级 UI，避免整棵应用崩溃。

```tsx
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error: unknown, info: React.ErrorInfo) {
    console.error('React subtree error', error, info.componentStack)
  }

  render() {
    if (this.state.hasError) {
      return <section role="alert">当前区域暂时不可用</section>
    }

    return this.props.children
  }
}
```

使用方式：

```tsx
function App() {
  return (
    <ErrorBoundary>
      <Dashboard />
    </ErrorBoundary>
  )
}
```

错误边界不能捕获所有错误。事件处理函数、异步回调、Promise、服务端渲染过程中的错误，需要各自处理。

```tsx
function SaveButton() {
  async function handleClick() {
    try {
      await saveForm()
    } catch (error) {
      console.error(error)
    }
  }

  return <button onClick={handleClick}>保存</button>
}
```

错误边界适合按页面、模块或关键区域布置。不要只在应用最外层放一个边界，否则用户只能看到整页降级，定位和恢复粒度都太粗。

## React 服务端渲染

React 服务端渲染是指在服务端把组件渲染成 HTML 字符串或流，浏览器先拿到可展示内容，再加载 JavaScript 进行 hydration，把静态 HTML 绑定成可交互应用。

基本流程：

1. 服务端接收请求。
2. 准备路由和数据。
3. 把 React 组件渲染成 HTML。
4. 浏览器展示 HTML。
5. 客户端加载 JavaScript。
6. React 执行 hydration，接管已有 DOM。

```tsx
import { renderToPipeableStream } from 'react-dom/server'

function handleRequest(res: {
  setHeader: (name: string, value: string) => void
}) {
  const stream = renderToPipeableStream(<App />, {
    onShellReady() {
      res.setHeader('content-type', 'text/html')
      stream.pipe(res as never)
    },
    onError(error) {
      console.error(error)
    }
  })
}
```

SSR 的优势包括首屏内容更快、SEO 更友好、可以流式传输。代价是服务端复杂度上升，需要处理数据预取、缓存、同构差异、hydration 不一致、部署成本和安全边界。

### hydration 不一致

hydration 要求服务端 HTML 和客户端首次渲染结果一致。下面这些情况容易造成不一致：

| 原因 | 处理方式 |
| --- | --- |
| 服务端和客户端时间不同 | 初始值从服务端注入，客户端提交后再刷新 |
| 依赖 `window` 或 `document` | 放到 effect 中执行 |
| 随机数直接参与渲染 | 服务端生成并注入稳定值 |
| 用户本地存储影响首屏 | 客户端挂载后再读取并更新 |

```tsx
function ClientOnlyTheme() {
  const [theme, setTheme] = React.useState<'light' | 'dark'>('light')

  React.useEffect(() => {
    const saved = window.localStorage.getItem('theme')
    if (saved === 'dark') {
      setTheme('dark')
    }
  }, [])

  return <span>{theme}</span>
}
```

这类代码让服务端首屏稳定，再在客户端提交后根据本地环境更新。

## 页面刷新后保留数据

页面刷新会清空内存中的 React state。保留数据要根据数据性质选择位置。

| 数据类型 | 推荐位置 |
| --- | --- |
| 筛选条件、分页、tab | URL query |
| 主题、语言 | localStorage 或 cookie |
| 临时表单草稿 | localStorage、sessionStorage、IndexedDB、服务端草稿 |
| 登录态 | 优先 HttpOnly Cookie |
| 权威业务数据 | 服务端重新拉取 |

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

能放进 URL 的状态优先放 URL，因为它支持刷新恢复、分享、收藏和浏览器前进后退。

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

敏感数据不要随意放到可被脚本读取的位置。

## 严格模式

React 严格模式通过 `<React.StrictMode>` 开启，只在开发环境执行额外检查，不影响生产构建行为。它用于发现不安全生命周期、意外副作用、旧字符串 ref、废弃 API 和清理缺失。

```tsx
import { createRoot } from 'react-dom/client'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

开发环境中，严格模式可能让某些函数或 effect 执行两次，用来暴露副作用不纯和清理不完整。不要简单把它当成框架问题，而应检查 effect 是否正确清理、render 是否保持纯计算。

```tsx
function OnlineStatus() {
  React.useEffect(() => {
    const handleOnline = () => console.log('online')
    window.addEventListener('online', handleOnline)

    return () => {
      window.removeEventListener('online', handleOnline)
    }
  }, [])

  return <span>状态监听中</span>
}
```

如果缺少清理函数，严格模式下更容易暴露重复订阅问题。

## React.Children 与 props.children

`props.children` 可能是单个元素、字符串、数字、数组、null 或其他可渲染值。不能默认把它当成数组处理。`React.Children` 提供了更安全的遍历、计数和转换工具。

```tsx
function Card({ children }: { children: React.ReactNode }) {
  return <section className="card">{children}</section>
}
```

遍历 children：

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

如果组件要求只有一个子元素，可以使用 `React.Children.only(children)`。这常见于触发器组件、动画组件和需要克隆子元素的组件。

```tsx
function Trigger({ children }: { children: React.ReactElement }) {
  const onlyChild = React.Children.only(children)

  return React.cloneElement(onlyChild, {
    'data-trigger': true
  })
}
```

克隆元素时要谨慎合并 props，避免覆盖调用方传入的事件、className 或 ref。

## 全局 Dialog 实现

全局 Dialog 通常由状态管理入口、Portal 渲染层和调用 API 组成。

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
        <GlobalDialog title={dialog.title} onClose={api.close}>
          {dialog.content}
        </GlobalDialog>
      ) : null}
    </DialogContext.Provider>
  )
}
```

Dialog 渲染层通常使用 Portal：

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

全局弹窗要处理焦点管理、Esc 关闭、滚动锁定、层级、动画和卸载清理。

## React 常见问题与解决方式

React 常见问题与解决方式可以按症状归类。

| 现象 | 常见原因 | 处理方式 |
| --- | --- | --- |
| 列表输入框内容串行 | 使用下标 key | 使用稳定业务 id |
| effect 读取旧状态 | 依赖数组缺失或闭包旧值 | 补完整依赖、函数式更新、使用 ref |
| 状态更新后马上读取旧值 | 把状态更新当同步赋值 | 在下一次渲染或 effect 中读取 |
| 子组件频繁渲染 | 父组件重渲染、props 引用不稳定 | 拆分组件、memo、稳定回调 |
| 表单值不更新 | 受控组件缺少 onChange | 同时维护 value 和更新函数 |
| 路由刷新 404 | BrowserRouter 缺少服务端回退 | 配置回退或使用 HashRouter |
| hydration 警告 | 服务端和客户端首屏不一致 | 稳定首屏值，客户端 effect 后更新 |
| 样式污染 | 全局 CSS 命名冲突 | CSS Modules、命名规范或作用域方案 |

### 直接修改状态

直接修改状态不会可靠触发更新，也会破坏浅比较。

```tsx
// 不推荐
user.name = 'Lin'
setUser(user)

// 推荐
setUser((prev) => ({
  ...prev,
  name: 'Lin'
}))
```

### effect 无限执行

effect 中依赖了每次 render 都新建的对象或函数，容易重复执行。

```tsx
function BadEffect({ keyword }: { keyword: string }) {
  const options = { keyword }

  React.useEffect(() => {
    loadData(options)
  }, [options])

  return null
}
```

可以把对象创建移动到 effect 内部，或用 `useMemo` 稳定引用。

```tsx
function GoodEffect({ keyword }: { keyword: string }) {
  React.useEffect(() => {
    loadData({ keyword })
  }, [keyword])

  return null
}
```

### async effect 写法

effect 回调本身不应直接声明为 async，因为 async 函数返回 Promise，而 effect 期望返回清理函数或 undefined。

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

## 工程实践检查清单

| 主题 | 建议 |
| --- | --- |
| 错误捕获 | 用错误边界隔离页面或模块，事件和异步单独处理 |
| SSR | 关注数据预取、hydration、一致性和缓存 |
| 持久化 | URL 表达可分享状态，敏感数据谨慎存储 |
| 严格模式 | 把重复执行视为副作用检查信号 |
| children | 使用 `React.Children` 安全处理不确定结构 |
| Dialog | Portal 渲染并处理焦点、滚动、键盘和层级 |
| 常见问题 | 从数据流、key、依赖、引用和部署回退角度定位 |

