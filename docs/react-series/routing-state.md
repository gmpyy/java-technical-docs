---
title: React 路由与状态管理
description: 整理 Redux、middleware、Redux 项目结构、React Router、Router 模式和 immutable 在 React 中的应用。
outline: [2, 3]
---

# React 路由与状态管理

React 本身负责 UI 组件模型，但真实应用还需要处理 URL、页面切换、跨组件状态、异步请求和数据一致性。React Router 解决 URL 与组件树的映射，Redux 解决可预测的集中式状态管理，immutable 思路则帮助 React 更可靠地判断变化。

## Redux 理解与工作原理

Redux 是可预测状态容器。它把跨组件共享的业务状态放入单一 store，通过 action 描述变化，通过 reducer 纯函数计算新 state。

Redux 的核心约束是：

| 约束 | 说明 |
| --- | --- |
| 单一 store | 应用共享状态集中管理 |
| state 只读 | 不直接修改旧状态 |
| action 描述变化 | 每次变化都有明确事件记录 |
| reducer 纯函数 | 根据旧 state 和 action 返回新 state |

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

基本工作流程：

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

Redux 适合共享状态复杂、需要统一调试、需要中间件处理异步流程的项目。简单局部交互状态不应为了统一而放进 Redux。

## Redux middleware

Redux middleware 是增强 dispatch 的机制。它可以拦截 action，在 action 到达 reducer 之前或之后增加日志、异步、错误处理、埋点和请求编排能力。

经典 middleware 签名是三层柯里化：

```ts
const logger = (store: {
  getState: () => unknown
}) => (next: (action: unknown) => unknown) => (action: unknown) => {
  console.log('before', store.getState())
  const result = next(action)
  console.log('after', store.getState())
  return result
}
```

三层参数分别表示：

| 参数 | 含义 |
| --- | --- |
| store | 包含 `getState` 和 `dispatch` 的 middleware API |
| next | 下一个 middleware 或原始 dispatch |
| action | 当前被派发的 action |

异步请求可以通过 thunk 这类 middleware 表达：

```ts
function loadUser(id: string) {
  return async (dispatch: (action: unknown) => void) => {
    dispatch({ type: 'user/loading', payload: id })

    try {
      const user = await fetchUser(id)
      dispatch({ type: 'user/success', payload: user })
    } catch (error) {
      dispatch({ type: 'user/error', payload: String(error) })
    }
  }
}
```

无论用 thunk、saga、observable 还是其他方案，都要把请求中、成功、失败、取消或过期这些状态表达清楚。

## React 项目中的 Redux 使用与结构划分

React 项目中的 Redux 使用通常包含 store 配置、模块 reducer、action 或 slice、selector、组件绑定层和异步逻辑。

一个可维护的结构可以按业务模块组织：

```text
src/
  app/
    store.ts
  features/
    user/
      userSlice.ts
      userSelectors.ts
      userApi.ts
      UserPanel.tsx
    cart/
      cartSlice.ts
      cartSelectors.ts
      CartSummary.tsx
```

使用 Redux Toolkit 时，slice 能把 action creator 和 reducer 组织在一起：

```ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

type CartState = {
  items: Array<{ id: string; count: number }>
}

const cartSlice = createSlice({
  name: 'cart',
  initialState: { items: [] } as CartState,
  reducers: {
    addItem(state, action: PayloadAction<string>) {
      state.items.push({ id: action.payload, count: 1 })
    }
  }
})

export const { addItem } = cartSlice.actions
export const cartReducer = cartSlice.reducer
```

Redux Toolkit 内部通过 Immer 支持“看起来像修改”的写法，最终仍会生成不可变更新。

组件中读取状态：

```tsx
function CartBadge() {
  const count = useSelector((state: RootState) => {
    return state.cart.items.length
  })
  const dispatch = useDispatch()

  return (
    <button onClick={() => dispatch(addItem('sku-1'))}>
      购物车：{count}
    </button>
  )
}
```

项目结构应让业务边界清晰。不要把所有 action、reducer、selector 都堆进全局目录，也不要让组件到处知道 store 的内部结构。

## connect 与 Hooks 绑定

`connect` 是 React-Redux 早期常用的高阶组件。它通过 `mapStateToProps` 和 `mapDispatchToProps` 把 store 数据和 dispatch 方法映射成组件 props。

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

现代项目更多使用 `useSelector` 和 `useDispatch`。但理解 `connect` 有助于维护旧项目，也能理解高阶组件如何把外部 store 映射到 React 组件树。

## Redux 请求并发处理

请求并发是状态管理中的常见难点。常见策略包括 requestId、取消旧请求、只保留最后一次结果、按资源 key 缓存请求状态。

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

并发策略要先由业务定义：搜索框通常保留最后一次结果，批量任务可能需要并行展示多个请求。

## React Router 理解与常用组件

React Router 让 URL 状态和 React 组件树对应。地址变化时，Router 匹配路由配置，渲染对应组件，而不是让浏览器整页刷新。

```tsx
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  Navigate,
  Outlet
} from 'react-router-dom'

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/users/:id" element={<UserDetail />} />
        <Route path="/admin" element={<AdminLayout />}>
          <Route path="users" element={<UserAdmin />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
```

常用组件和 Hook：

| API | 用途 |
| --- | --- |
| `BrowserRouter` | 使用 History API 管理路由 |
| `Routes` | 选择匹配的路由分支 |
| `Route` | 声明路径和组件映射 |
| `Link` | 站内跳转，不整页刷新 |
| `Navigate` | 声明式重定向 |
| `Outlet` | 嵌套路由出口 |
| `useParams` | 读取路径参数 |
| `useSearchParams` | 读取和写入查询参数 |
| `useNavigate` | 命令式跳转 |

## Link 与 a 标签

`Link` 用于站内路由跳转，会拦截点击并通过 history 更新地址。普通 `a` 标签默认触发浏览器导航，适合下载、外链或确实需要整页刷新。

```tsx
function Nav() {
  return (
    <nav>
      <Link to="/users">用户</Link>
      <a href="/download/report.csv">下载报表</a>
    </nav>
  )
}
```

站内页面跳转优先使用 `Link`，文件下载和外部地址使用 `a`。

## React Router 模式与实现原理

React Router 常见模式包括 BrowserRouter、HashRouter、MemoryRouter 和 StaticRouter。

| 模式 | 实现基础 | 场景 |
| --- | --- | --- |
| BrowserRouter | History API | 普通 Web 应用，URL 自然 |
| HashRouter | URL hash | 静态托管、服务端无法配置回退 |
| MemoryRouter | 内存中的路由栈 | 单元测试、非浏览器容器 |
| StaticRouter | 静态上下文 | 服务端渲染 |

```tsx
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

BrowserRouter 部署时，服务端需要把未知路径回退到入口 HTML。静态托管如果无法配置回退，HashRouter 更省事。文档站使用 VitePress 时，路由构建由 VitePress 处理。

## 路由参数变化与组件复用

同一个路由组件只是参数变化时，组件可能保留局部状态。需要根据参数重新请求数据时，应监听参数。

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

如果希望参数变化时强制重新创建组件，可以在包装层传 key。

```tsx
function ArticleRoute() {
  const { id } = useParams()
  return <ArticlePage key={id} />
}
```

## immutable 在 React 中的应用

immutable 在 React 中的应用重点是不可变更新。React 的很多优化依赖引用比较：`PureComponent`、`React.memo`、`useMemo`、`useCallback` 和 selector 缓存都需要稳定且正确的引用变化。

```tsx
// 不推荐：原数组引用不变
items.push(nextItem)
setItems(items)

// 推荐：创建新数组引用
setItems((prev) => [...prev, nextItem])
```

对象更新也要创建新引用：

```tsx
setUser((prev) => ({
  ...prev,
  profile: {
    ...prev.profile,
    nickname: 'Lin'
  }
}))
```

不可变更新的价值：

| 价值 | 说明 |
| --- | --- |
| 变化可追踪 | 旧值和新值可以比较 |
| 浅比较有效 | 引用变化能表达数据变化 |
| 回滚和调试 | 可以保留历史状态 |
| 选择器缓存 | 相同输入可以复用计算结果 |

不可变不是要求手写大量展开。复杂嵌套状态可以使用 Immer、Redux Toolkit 或重新设计状态结构，让更新路径更短。

## Redux、MobX 与 Vuex

Redux、MobX 和 Vuex 都在解决共享状态问题，但理念不同。

| 方案 | 特点 |
| --- | --- |
| Redux | action + reducer，强调不可变、可追踪、流程规范 |
| MobX | 响应式可观察数据，写法直接，依赖追踪自动 |
| Vuex | 面向 Vue 生态的集中式状态管理，结合 Vue 响应式 |

Redux 更适合团队强调流程、调试和状态可预测的场景；MobX 更适合数据模型复杂但希望写法直接的场景。选择状态库前，应先确认问题是否已经超出局部 state、Context 或请求缓存的范围。

## 路由与状态管理检查清单

| 主题 | 建议 |
| --- | --- |
| Redux | 只管理真正跨组件、跨页面、需要追踪的状态 |
| reducer | 保持纯函数，不发请求、不改旧 state |
| middleware | 用于异步、日志、错误和流程增强 |
| 项目结构 | 按业务模块组织 slice、selector、组件和 API |
| Router | 用 URL 表达可分享、可恢复的页面状态 |
| Link | 站内跳转用 Link，下载和外部地址用 a |
| Router 模式 | 根据部署环境选择 BrowserRouter 或 HashRouter |
| immutable | 保持引用变化可靠，服务于浅比较和调试 |

