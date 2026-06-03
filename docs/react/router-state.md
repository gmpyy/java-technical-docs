---
title: React 通信、路由与状态管理
description: 整理组件通信、props 层级问题、React-Router、Redux、middleware、connect、MobX 与 Vuex。
outline: [2, 3]
---

# React 通信、路由与状态管理

真实项目中的 React 不只包含组件渲染，还要处理组件间数据流、页面路由、共享状态、异步请求和工程边界。通信解决“组件之间怎么传递信息”，路由解决“URL 和页面状态怎么对应”，状态管理解决“跨页面、跨层级、跨业务模块的数据如何统一维护”。

## 组件通信方式总览

React 默认是单向数据流：父组件通过 props 向子组件传数据，子组件通过回调把事件交给父组件。随着层级变深或组件关系变复杂，可以选择 Context、发布订阅、外部 store、路由状态或缓存层。

| 关系 | 常见方式 |
| --- | --- |
| 父子组件 | props、回调函数、ref |
| 跨级组件 | Context、组合插槽、状态提升 |
| 非嵌套组件 | 发布订阅、外部 store、URL、缓存、共同父级 |
| 多页面共享 | Redux、Context + reducer、数据请求缓存、浏览器存储 |

通信方案没有唯一答案，应根据数据的生命周期、更新频率、影响范围和可追踪性选择。

## 父子组件通信

父组件向子组件传数据，子组件通过回调通知父组件，这是一切通信方式的基础。

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

如果父组件需要调用子组件的命令式方法，可以使用 `ref`、`forwardRef` 和 `useImperativeHandle`。

```tsx
type InputHandle = {
  focus: () => void
}

const SmartInput = React.forwardRef<InputHandle>((props, ref) => {
  const inputRef = React.useRef<HTMLInputElement | null>(null)

  React.useImperativeHandle(ref, () => ({
    focus() {
      inputRef.current?.focus()
    }
  }))

  return <input ref={inputRef} />
})
```

命令式 ref 应少用。能通过 props 表达的数据流，不要改成父组件直接操纵子组件。

## 跨级组件通信

跨级通信最常见的是 Context。它适合主题、语言、权限、登录用户等需要被多层组件读取的数据。

```tsx
const AuthContext = React.createContext<{
  userId: string
  role: string
} | null>(null)

function CurrentUser() {
  const auth = React.useContext(AuthContext)
  return <span>{auth?.userId}</span>
}
```

如果只是为了传递某块 UI，也可以通过组件组合减少 props 层级。

```tsx
function Layout({ header, children }: {
  header: React.ReactNode
  children: React.ReactNode
}) {
  return (
    <>
      <header>{header}</header>
      <main>{children}</main>
    </>
  )
}
```

组合方式的好处是依赖更显式。Context 的好处是跨层级读取方便，但更新影响范围更大。

## 非嵌套组件通信

非嵌套组件没有直接父子关系，常见方案包括共同父级状态、发布订阅、外部 store 和 URL。

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

发布订阅适合低耦合事件，例如全局通知、埋点、微前端消息。但业务核心状态如果大量依赖事件总线，容易让数据来源不可追踪。更稳定的做法是把共享状态放到 store 或共同父级。

## 解决 props 层级过深

props 层级过深通常被称为 props drilling。解决方案有四类：

| 方案 | 适合场景 |
| --- | --- |
| 组件组合 | 中间层只负责布局，不需要理解数据 |
| 状态提升 | 多个兄弟组件共享同一份局部状态 |
| Context | 跨多层读取低频全局数据 |
| 状态管理库 | 复杂业务共享状态、异步流程、调试追踪 |

```tsx
function Page() {
  return (
    <Toolbar
      actions={<SaveButton />}
      profile={<UserProfile />}
    />
  )
}
```

通过把子元素作为 props 传入，可以让中间组件不再层层转发大量业务 props。

## React-Router 实现原理

React-Router 的核心是让 URL 状态与 React 组件树对应。它监听浏览器地址变化，匹配路由配置，渲染对应组件。不同模式使用不同浏览器能力：BrowserRouter 使用 History API，HashRouter 使用 URL hash。

```tsx
import {
  BrowserRouter,
  Routes,
  Route
} from 'react-router-dom'

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/users/:id" element={<UserDetail />} />
      </Routes>
    </BrowserRouter>
  )
}
```

路由切换时，React-Router 并不会让浏览器整页刷新，而是更新 history，通知 Router 重新匹配，React 再渲染新的路由组件。

## 路由切换配置

React-Router v6 使用 `Routes` 和 `Route`。每个 `Route` 描述 path 和 element。嵌套路由可以用 `Outlet`。

```tsx
import { Outlet } from 'react-router-dom'

function AdminLayout() {
  return (
    <>
      <nav>后台导航</nav>
      <Outlet />
    </>
  )
}

function AppRouter() {
  return (
    <Routes>
      <Route path="/admin" element={<AdminLayout />}>
        <Route path="users" element={<UserAdmin />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  )
}
```

路由配置应该和页面结构保持一致。大型项目可以按业务模块拆分路由，配合懒加载降低首屏包体。

## 重定向

React-Router v6 中可以使用 `Navigate` 做声明式重定向，也可以在事件或 effect 中使用 `useNavigate` 命令式跳转。

```tsx
import { Navigate, useNavigate } from 'react-router-dom'

function ProtectedPage({ loggedIn }: { loggedIn: boolean }) {
  if (!loggedIn) {
    return <Navigate to="/login" replace />
  }

  return <Dashboard />
}

function LoginButton() {
  const navigate = useNavigate()

  return (
    <button onClick={() => navigate('/dashboard')}>
      进入控制台
    </button>
  )
}
```

`replace` 表示替换当前历史记录，适合登录态拦截，避免用户点击返回又回到无权限页面。

## Link 与 a 标签

`Link` 和普通 `a` 标签的区别在于：`Link` 会拦截点击并使用 history 更新地址，从而避免整页刷新；`a` 标签默认会让浏览器重新请求页面。

```tsx
import { Link } from 'react-router-dom'

function Nav() {
  return (
    <nav>
      <Link to="/users">用户</Link>
      <a href="/download/report.csv">下载报表</a>
    </nav>
  )
}
```

站内路由跳转用 `Link`，文件下载、外部页面或确实需要浏览器默认行为时用 `a`。

## URL 参数与 history 对象

React-Router v6 中，路径参数用 `useParams`，查询参数用 `useSearchParams`，导航能力用 `useNavigate`。

```tsx
import {
  useNavigate,
  useParams,
  useSearchParams
} from 'react-router-dom'

function UserDetail() {
  const { id } = useParams()
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  return (
    <>
      <p>用户：{id}</p>
      <p>tab：{searchParams.get('tab')}</p>
      <button onClick={() => navigate(-1)}>返回</button>
    </>
  )
}
```

旧版本中常见的 history 对象，在新版本中主要通过 `useNavigate` 表达。维护旧项目时仍可能看到 `props.history.push` 或 `withRouter`。

## 同一个组件在路由变化时重新渲染

当同一个路由组件只是参数变化时，组件可能复用实例或保持局部状态。需要根据参数重新请求数据时，应监听参数变化。

```tsx
function ArticlePage() {
  const { id } = useParams()
  const [article, setArticle] = React.useState<{ title: string } | null>(null)

  React.useEffect(() => {
    if (!id) {
      return
    }

    loadArticle(id).then(setArticle)
  }, [id])

  return <h1>{article?.title}</h1>
}
```

如果确实希望参数变化时强制重新创建组件，可以在路由包装层传入 key。

```tsx
function ArticleRoute() {
  const { id } = useParams()
  return <ArticlePage key={id} />
}
```

## 路由模式

React-Router 常见模式包括 BrowserRouter、HashRouter、MemoryRouter、StaticRouter。

| 模式 | 说明 | 场景 |
| --- | --- | --- |
| BrowserRouter | 使用 History API，URL 更自然 | 普通 Web 应用 |
| HashRouter | 使用 `#` 后内容，不依赖服务端回退 | 静态部署、旧环境 |
| MemoryRouter | 路由存在内存中 | 单元测试、非浏览器容器 |
| StaticRouter | 静态渲染场景 | SSR |

BrowserRouter 部署时，服务端需要把未知路径回退到入口 HTML。GitHub Pages 这类静态托管如果没有额外回退配置，HashRouter 会更省心；VitePress 本身已经处理文档站路由构建。

## Switch 与 Routes

React-Router 4/5 中的 `Switch` 用来只渲染第一个匹配的路由，避免多个路由同时命中。React-Router v6 中 `Switch` 被 `Routes` 替代，匹配算法也更明确。

```tsx
// React-Router 4/5 写法
function LegacyRoutes() {
  return (
    <Switch>
      <Route exact path="/" component={Home} />
      <Route path="/users/:id" component={UserDetail} />
      <Route component={NotFound} />
    </Switch>
  )
}
```

维护旧项目时看到 `Switch`，要理解它的作用是“只选择一个分支”。新项目使用 v6 写法即可。

## Redux 的定位

Redux 是可预测状态容器，主要解决跨组件共享状态、复杂数据流、统一调试和异步流程组织问题。它的核心约束是：单一 store、只读 state、通过 action 描述变化、reducer 纯函数计算新 state。

```ts
type CounterState = {
  count: number
}

type CounterAction =
  | { type: 'counter/increment' }
  | { type: 'counter/add'; payload: number }

function counterReducer(
  state: CounterState = { count: 0 },
  action: CounterAction
): CounterState {
  switch (action.type) {
    case 'counter/increment':
      return { count: state.count + 1 }
    case 'counter/add':
      return { count: state.count + action.payload }
    default:
      return state
  }
}
```

Redux 适合状态共享复杂、需要时间旅行调试、需要中间件处理异步和日志的项目。简单局部状态不必上 Redux。

## Redux 工作流程

Redux 的基本流程是：

1. 组件 dispatch action。
2. store 把当前 state 和 action 交给 reducer。
3. reducer 返回新 state。
4. store 保存新 state 并通知订阅者。
5. React 绑定层重新选择数据并触发组件更新。

```ts
store.dispatch({
  type: 'counter/add',
  payload: 2
})

const state = store.getState()
console.log(state.counter.count)
```

reducer 必须是纯函数，不应该发请求、写本地存储、改外部变量或直接修改旧 state。

## Redux 异步请求

Redux 本身只处理同步 action。异步请求通常通过 middleware 扩展，例如 thunk、saga、observable 或 Redux Toolkit 的 async thunk。

```ts
function loadUser(id: string) {
  return async (dispatch: (action: unknown) => void) => {
    dispatch({ type: 'user/loading' })

    try {
      const user = await fetchUser(id)
      dispatch({ type: 'user/success', payload: user })
    } catch (error) {
      dispatch({ type: 'user/error', payload: String(error) })
    }
  }
}
```

异步 action 的关键是把“请求中、成功、失败”都变成明确状态。组件不直接猜测请求处于哪个阶段，而是从 store 读取状态。

## Redux middleware

Redux middleware 是增强 dispatch 的函数。它的经典签名是三层柯里化：

```ts
const logger: Middleware = (store) => (next) => (action) => {
  console.log('before', store.getState())
  const result = next(action)
  console.log('after', store.getState())
  return result
}
```

三层参数分别是：

| 参数 | 含义 |
| --- | --- |
| `store` | 包含 `getState` 和 `dispatch` 的 middleware API |
| `next` | 下一个 middleware 或原始 dispatch |
| `action` | 当前被派发的 action |

middleware 能拿到 store 和 action，是因为 `applyMiddleware` 在创建 store 时把 middleware 串成链，并把增强后的 dispatch 暴露给应用。

## 请求并发处理

Redux 请求并发需要明确策略。常见做法包括按 requestId 忽略过期结果、使用 AbortController 取消旧请求、使用 saga 的 `takeLatest`、按资源 key 缓存请求状态。

```ts
type UserState = {
  requestId: string | null
  data: unknown
}

function userReducer(state: UserState, action: {
  type: string
  payload?: unknown
  meta?: { requestId: string }
}): UserState {
  if (action.type === 'user/request') {
    return { ...state, requestId: action.meta?.requestId ?? null }
  }

  if (action.type === 'user/success') {
    if (state.requestId !== action.meta?.requestId) {
      return state
    }

    return { ...state, data: action.payload }
  }

  return state
}
```

并发问题不只是技术细节，也关系到产品语义：是保留最后一次搜索结果，还是多个请求并行展示，应该由业务定义。

## Redux 与 window 变量

把变量挂到 `window` 上也能跨组件访问，但它和 Redux 有本质差异。

| 维度 | window 变量 | Redux |
| --- | --- | --- |
| 更新通知 | 无标准订阅机制 | store 订阅更新 |
| 可追踪性 | 难知道谁改了 | action 可记录 |
| 调试工具 | 基本没有 | 可接入 DevTools |
| 数据约束 | 任意读写 | reducer 统一计算 |
| React 集成 | 需要手动触发渲染 | 绑定层自动映射到组件 |

window 适合放极少量环境信息或调试开关，不适合承载业务状态。

## connect 的作用

`connect` 是 React-Redux 中把 Redux store 与 React 组件连接起来的高阶组件。它接收 `mapStateToProps` 和 `mapDispatchToProps`，把 store 中的数据和 dispatch 方法映射成组件 props。

```tsx
import { connect } from 'react-redux'

function CounterView(props: {
  count: number
  increase: () => void
}) {
  return <button onClick={props.increase}>{props.count}</button>
}

const mapStateToProps = (state: { counter: { count: number } }) => ({
  count: state.counter.count
})

const mapDispatchToProps = {
  increase: () => ({ type: 'counter/increment' })
}

export const Counter = connect(
  mapStateToProps,
  mapDispatchToProps
)(CounterView)
```

现代 React-Redux 更常使用 `useSelector` 和 `useDispatch`，但理解 `connect` 仍然有助于维护旧项目和理解高阶组件模式。

## Redux 属性传递原理

Redux 属性传递不是神秘注入。Provider 把 store 放入 React Context；`connect` 或 Hook 从 Context 中读取 store，订阅 store 变化，执行 selector 或 `mapStateToProps`，再把结果作为 props 或 Hook 返回值交给组件。

```tsx
import { Provider, useSelector } from 'react-redux'

function CountText() {
  const count = useSelector((state: { counter: { count: number } }) => {
    return state.counter.count
  })

  return <span>{count}</span>
}

function Root({ store }: { store: unknown }) {
  return (
    <Provider store={store}>
      <CountText />
    </Provider>
  )
}
```

这个过程最终仍然回到 React 的渲染模型：外部 store 变化被转成组件读取值的变化。

## MobX 与 Redux

MobX 和 Redux 都能管理状态，但理念不同。

| 维度 | Redux | MobX |
| --- | --- | --- |
| 数据变化 | action + reducer 显式计算 | 响应式可观察数据自动追踪 |
| 样板代码 | 较多，但流程清晰 | 较少，写法接近直接修改 |
| 可预测性 | 强，变化路径统一 | 灵活，但大型项目要约束 |
| 调试 | action 记录清晰 | 依赖响应式追踪工具 |
| 学习重点 | 不可变数据、reducer、middleware | observable、computed、action |

Redux 更适合强调流程规范和可追踪的大型团队；MobX 更适合数据模型复杂但希望写法直接的场景。两者都需要团队约定。

## Redux 与 Vuex

Redux 和 Vuex 的共同思想是集中式状态管理：把跨组件共享状态放到一个统一位置，通过明确方式修改状态，再让视图响应变化。

| 维度 | Redux | Vuex |
| --- | --- | --- |
| 框架关系 | 与 React 解耦，可用于其他环境 | 面向 Vue 生态 |
| 修改方式 | dispatch action，reducer 返回新状态 | commit mutation，action 处理异步 |
| 数据原则 | 强调不可变更新 | 基于 Vue 响应式 |
| 模块化 | reducer 拆分 | module 拆分 |

它们都强调单向数据流、集中调试和状态可追踪，只是结合各自框架的响应机制采用了不同 API。

## 状态管理选择建议

| 场景 | 建议 |
| --- | --- |
| 单个组件局部交互 | `useState` |
| 多个相关状态且更新逻辑复杂 | `useReducer` |
| 跨层级低频配置 | Context |
| 跨页面共享业务状态 | Redux、Zustand、MobX 等 |
| 服务端数据缓存 | 查询缓存库或框架数据层 |
| URL 可表达的状态 | 路由参数或查询参数 |

状态不要为了共享而共享。状态离使用它的地方越近，理解成本越低；只有当多个地方确实需要同一份数据时，才提升或放入共享层。

