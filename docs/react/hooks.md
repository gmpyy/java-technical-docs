---
title: React Hooks
description: 整理 React Hooks 的设计目的、实现心智模型、使用限制、常用 Hook、闭包问题和生命周期对应关系。
outline: [2, 3]
---

# React Hooks

React Hooks 让函数组件拥有状态、副作用、引用、缓存和逻辑复用能力。它不是简单地替换类组件语法，而是改变了组织组件逻辑的方式：同一业务逻辑可以写在一起，不必拆散到多个生命周期方法中；可复用逻辑可以抽成普通函数，不必依赖 HOC 或 Render props。

## React Hook 的理解与实现心智模型

Hook 是 React 在函数组件渲染期间维护的一组状态单元。每次组件执行时，React 按 Hook 调用顺序把当前调用和内部链表或数组中的状态位置对应起来。因此 Hook 必须在组件顶层稳定调用，不能放在条件、循环或普通嵌套函数中。

```tsx
function Profile() {
  const [name, setName] = React.useState('Lin')
  const [age, setAge] = React.useState(18)

  return (
    <button onClick={() => setAge((value) => value + 1)}>
      {name} - {age}
    </button>
  )
}
```

可以把这个过程理解为：第一次渲染时，React 为第一个 `useState` 保存 `name`，为第二个 `useState` 保存 `age`；下一次渲染时，必须仍然按相同顺序调用，React 才能把状态取回到正确位置。

```tsx
// 不推荐：条件分支会破坏 Hook 顺序
function BadExample({ enabled }: { enabled: boolean }) {
  if (enabled) {
    const [count, setCount] = React.useState(0)
    return <button onClick={() => setCount(count + 1)}>{count}</button>
  }

  return null
}
```

正确写法是把条件放在 Hook 内部或 Hook 之后。

```tsx
function GoodExample({ enabled }: { enabled: boolean }) {
  const [count, setCount] = React.useState(0)

  if (!enabled) {
    return null
  }

  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

## useState

`useState` 用于在函数组件中保存局部状态。初始值可以直接传值，也可以传入函数进行惰性初始化。

```tsx
function TodoList() {
  const [items, setItems] = React.useState<string[]>(() => {
    return ['学习 React', '整理文档']
  })

  function addItem(text: string) {
    setItems((prev) => [...prev, text])
  }

  return (
    <ul>
      {items.map((item) => <li key={item}>{item}</li>)}
      <button onClick={() => addItem('复盘代码')}>新增</button>
    </ul>
  )
}
```

`useState` 返回数组而不是对象，主要是为了调用方可以自由命名。一个组件可以多次调用 `useState`，数组解构让每个状态都有自己的命名空间。

```tsx
const [count, setCount] = React.useState(0)
const [visible, setVisible] = React.useState(true)
const [keyword, setKeyword] = React.useState('')
```

如果返回对象，调用方要么固定字段名，要么额外重命名，组合多个 Hook 时会更别扭。

## useEffect

`useEffect` 用于处理渲染提交后的副作用，例如请求数据、订阅事件、同步标题、写入存储等。它默认在浏览器完成绘制后执行，不阻塞首屏绘制。

```tsx
function DocumentTitle({ title }: { title: string }) {
  React.useEffect(() => {
    document.title = title
  }, [title])

  return <h1>{title}</h1>
}
```

effect 返回的函数用于清理上一次副作用或卸载时释放资源。

```tsx
function OnlineStatus() {
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

  return <span>{online ? '在线' : '离线'}</span>
}
```

依赖数组表达“这个副作用依赖哪些渲染值”。少写依赖可能读到旧值，多写不稳定引用可能导致频繁执行。不要把依赖数组当成手动开关，而应让它真实反映 effect 内用到的响应式值。

## useLayoutEffect

`useLayoutEffect` 和 `useEffect` 的区别在于执行时机。`useLayoutEffect` 在 DOM 更新后、浏览器绘制前同步执行；`useEffect` 通常在绘制后异步执行。

```tsx
function MeasureBox() {
  const ref = React.useRef<HTMLDivElement | null>(null)
  const [height, setHeight] = React.useState(0)

  React.useLayoutEffect(() => {
    if (ref.current) {
      setHeight(ref.current.getBoundingClientRect().height)
    }
  }, [])

  return (
    <>
      <div ref={ref}>需要测量的内容</div>
      <span>高度：{height}</span>
    </>
  )
}
```

需要同步测量布局、修正滚动位置、避免闪烁时，使用 `useLayoutEffect`。普通数据请求、事件订阅、日志、标题同步等场景，应优先使用 `useEffect`，避免阻塞绘制。

## useMemo

`useMemo` 缓存计算结果。它适合昂贵计算或需要稳定引用传给子组件的值。不要为了“看起来专业”到处使用 `useMemo`，缓存本身也有成本。

```tsx
function ProductList({ products, keyword }: {
  products: Array<{ id: string; name: string }>
  keyword: string
}) {
  const filtered = React.useMemo(() => {
    return products.filter((product) => product.name.includes(keyword))
  }, [products, keyword])

  return (
    <ul>
      {filtered.map((product) => <li key={product.id}>{product.name}</li>)}
    </ul>
  )
}
```

如果计算很轻，直接计算通常更简单。`useMemo` 不能作为语义保证，React 未来也可能出于内部原因重新计算；它应该被视作性能优化工具。

## useCallback

`useCallback` 缓存函数引用，常和 `React.memo` 配合，避免子组件因回调引用变化而重新渲染。

```tsx
const UserRow = React.memo(function UserRow(props: {
  id: string
  onSelect: (id: string) => void
}) {
  return <button onClick={() => props.onSelect(props.id)}>{props.id}</button>
})

function UserTable({ ids }: { ids: string[] }) {
  const handleSelect = React.useCallback((id: string) => {
    console.log(id)
  }, [])

  return (
    <>
      {ids.map((id) => (
        <UserRow key={id} id={id} onSelect={handleSelect} />
      ))}
    </>
  )
}
```

`useCallback(fn, deps)` 可以理解为 `useMemo(() => fn, deps)`。它解决的是函数引用稳定性，不会自动让函数内部读取到最新值。涉及闭包时仍要正确写依赖或使用函数式更新。

## useRef

`useRef` 返回一个稳定对象，`ref.current` 可以保存 DOM，也可以保存跨渲染可变值。修改 `ref.current` 不会触发组件重新渲染。

```tsx
function ClickCounter() {
  const countRef = React.useRef(0)

  function handleClick() {
    countRef.current += 1
    console.log(countRef.current)
  }

  return <button onClick={handleClick}>记录点击次数</button>
}
```

如果值改变需要立刻反映到界面，应使用 state；如果只是保存定时器 id、上一次值、DOM 节点、外部实例，使用 ref 更合适。

```tsx
function PreviousValue({ value }: { value: string }) {
  const previous = React.useRef<string | undefined>(undefined)

  React.useEffect(() => {
    previous.current = value
  }, [value])

  return <span>上一次：{previous.current ?? '无'}</span>
}
```

## 自定义 Hook

自定义 Hook 是以 `use` 开头的函数，可以调用其他 Hook。它让状态逻辑和副作用逻辑复用成为普通函数组合。

```tsx
function useLocalStorageState(key: string, initialValue: string) {
  const [value, setValue] = React.useState(() => {
    return window.localStorage.getItem(key) ?? initialValue
  })

  React.useEffect(() => {
    window.localStorage.setItem(key, value)
  }, [key, value])

  return [value, setValue] as const
}

function NameEditor() {
  const [name, setName] = useLocalStorageState('name', '')

  return (
    <input
      value={name}
      onChange={(event) => setName(event.target.value)}
    />
  )
}
```

自定义 Hook 不共享状态本身，每次调用都会拥有独立的 Hook 状态。它共享的是逻辑结构。如果要共享同一份数据，需要 Context、外部 store 或其他状态源。

## Hooks 解决的问题

React Hooks 主要解决这些问题：

| 问题 | Hooks 带来的变化 |
| --- | --- |
| 类组件逻辑分散 | 相关逻辑可以放在同一个 effect 或自定义 Hook 中 |
| this 绑定复杂 | 函数组件不依赖实例 this |
| 逻辑复用嵌套深 | 自定义 Hook 比 HOC 和 Render props 更扁平 |
| 状态逻辑难组合 | Hook 是函数，可以组合、拆分和测试 |
| 生命周期语义过粗 | 副作用按依赖和清理组织，更贴近数据流 |

Hooks 并不让组件自动变快。它改善的是组织方式和复用方式，性能仍取决于状态设计、渲染范围、依赖稳定性和组件拆分。

## 使用限制

Hook 的限制可以总结为两条：

1. 只在 React 函数组件或自定义 Hook 中调用。
2. 只在顶层调用，不在条件、循环、嵌套函数中调用。

这些限制是实现模型决定的。React 依赖 Hook 调用顺序定位每个状态单元，一旦顺序变化，状态就会对应错位。

```tsx
function useFeatureFlag(flag: boolean) {
  const [enabled, setEnabled] = React.useState(flag)

  React.useEffect(() => {
    setEnabled(flag)
  }, [flag])

  return enabled
}
```

自定义 Hook 同样要遵守规则。只要函数名以 `use` 开头，相关检查工具就能帮助发现调用位置错误。

## 闭包与依赖

Hooks 开发中最常见的问题是闭包旧值。每次渲染都会创建新的函数和变量，effect 或回调捕获的是那一次渲染中的值。

```tsx
function IntervalCounter() {
  const [count, setCount] = React.useState(0)

  React.useEffect(() => {
    const timer = window.setInterval(() => {
      setCount((value) => value + 1)
    }, 1000)

    return () => window.clearInterval(timer)
  }, [])

  return <span>{count}</span>
}
```

这里使用函数式更新，避免定时器回调捕获初始 `count`。另一个常见方案是把最新值写入 ref。

```tsx
function useLatest<T>(value: T) {
  const ref = React.useRef(value)

  React.useEffect(() => {
    ref.current = value
  }, [value])

  return ref
}
```

依赖数组不是为了消除警告而存在，它表达 effect 的数据依赖。确实不想让某个函数成为依赖时，可以把逻辑移入 effect、使用函数式更新、使用 ref 保存命令式值，或把函数用 `useCallback` 稳定下来。

## Hooks 与生命周期关系

Hook 不等价于生命周期方法的一对一替换。函数组件每次渲染都是一次完整函数执行，effect 则在提交后处理副作用。

| 需求 | class 写法 | Hook 写法 |
| --- | --- | --- |
| 挂载后请求 | `componentDidMount` | `useEffect(..., [])` |
| 参数变化请求 | `componentDidUpdate` 比较 props | `useEffect(..., [id])` |
| 卸载清理 | `componentWillUnmount` | effect 返回清理函数 |
| DOM 测量 | `componentDidMount` / `componentDidUpdate` | `useLayoutEffect` |
| 避免子组件重复渲染 | `PureComponent` | `React.memo` + `useCallback` |

```tsx
function Article({ id }: { id: string }) {
  const [title, setTitle] = React.useState('')

  React.useEffect(() => {
    let active = true

    loadArticle(id).then((article) => {
      if (active) {
        setTitle(article.title)
      }
    })

    return () => {
      active = false
    }
  }, [id])

  return <h1>{title}</h1>
}
```

这段逻辑同时表达了挂载后请求、id 变化重新请求和清理过期请求，不需要拆到多个生命周期方法中。

## 开发注意点

| 注意点 | 原因 |
| --- | --- |
| 不在条件中调用 Hook | 保持调用顺序稳定 |
| 依赖数组真实完整 | 避免旧闭包和状态不同步 |
| 复杂对象谨慎作为依赖 | 引用每次变化会导致 effect 重复执行 |
| 状态更新依赖旧值时使用函数式写法 | 避免批处理中读取旧值 |
| 不滥用 useMemo/useCallback | 缓存有成本，优先定位瓶颈 |
| effect 做清理 | 避免内存泄漏、重复订阅和过期写入 |
| 自定义 Hook 保持单一职责 | 便于复用和测试 |

## Hooks 小结

React Hooks 的重点不只是记住 API，而是理解函数组件的渲染快照。每次渲染都有自己的 props、state、函数和 effect；状态更新会触发下一次渲染；effect 在提交后运行并可以清理上一次副作用。掌握这个模型后，`useState`、`useEffect`、`useMemo`、`useCallback`、`useRef` 和自定义 Hook 都会变得更容易判断。

