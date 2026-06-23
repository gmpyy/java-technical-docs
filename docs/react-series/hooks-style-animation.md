---
title: React Hooks、样式与动画
description: 整理 React Hooks 的设计目的、常用 API、闭包依赖、CSS 引入方式和组件过渡动画实现。
outline: [2, 3]
---

# React Hooks、样式与动画

Hooks 解决的是函数组件如何拥有状态、副作用、引用、缓存和逻辑复用能力。样式和动画解决的是组件如何呈现视觉状态。把这三类内容放在一起看，可以形成一个完整的 UI 开发视角：数据变化触发渲染，Hook 管理逻辑，样式和动画表达状态。

## React Hooks

React Hooks 是一组以 `use` 开头的函数，用于在函数组件中接入 React 的状态和生命周期能力。它的关键不是少写 class，而是让相关逻辑可以按功能聚合，而不是被拆散到多个生命周期方法中。

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

Hook 的实现心智模型是“按调用顺序保存状态单元”。每次组件执行时，React 按 Hook 出现顺序把调用和内部保存的位置对应起来。因此 Hook 必须稳定调用。

```tsx
function GoodExample({ enabled }: { enabled: boolean }) {
  const [count, setCount] = React.useState(0)

  if (!enabled) {
    return null
  }

  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

不要在条件、循环或普通嵌套函数中调用 Hook。条件可以写在 Hook 内部，或写在 Hook 调用之后。

## useState

`useState` 用于保存局部状态。初始值可以直接传入，也可以传入函数做惰性初始化。

```tsx
function TodoList() {
  const [items, setItems] = React.useState<string[]>(() => {
    return ['学习 React', '整理文档']
  })

  function addItem(text: string) {
    setItems((prev) => [...prev, text])
  }

  return (
    <>
      <button onClick={() => addItem('复盘代码')}>新增</button>
      <ul>{items.map((item) => <li key={item}>{item}</li>)}</ul>
    </>
  )
}
```

`useState` setter 不会像类组件 `setState` 那样自动浅合并对象。如果状态是对象，需要手动保留旧字段。

```tsx
const [form, setForm] = React.useState({ name: '', age: 0 })

setForm((prev) => ({
  ...prev,
  name: 'Chen'
}))
```

## useEffect

`useEffect` 用于处理提交后的副作用，例如请求、订阅、同步标题、写入存储、上报日志等。它默认在浏览器完成绘制后执行，不阻塞首屏绘制。

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

依赖数组表达 effect 使用了哪些响应式值。少写依赖会读到旧值，多写不稳定引用会频繁执行。不要把依赖数组当作手动开关。

## useLayoutEffect

`useLayoutEffect` 在 DOM 更新后、浏览器绘制前同步执行。它适合同步测量布局、修正滚动位置和避免视觉闪烁。

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

普通请求、日志、标题同步和订阅优先使用 `useEffect`，避免阻塞绘制。

## useMemo 与 useCallback

`useMemo` 缓存计算结果，`useCallback` 缓存函数引用。它们是性能工具，不是语义工具。

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

`useCallback(fn, deps)` 可以理解为 `useMemo(() => fn, deps)`。

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

不要为了“看起来优化”到处包缓存。缓存本身也有成本，只有计算昂贵或引用稳定性影响子组件渲染时才值得使用。

## useRef

`useRef` 返回一个稳定对象。`ref.current` 可以保存 DOM，也可以保存跨渲染可变值。修改 `ref.current` 不会触发重新渲染。

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

保存定时器 id、上一次值、DOM 节点、第三方库实例时，ref 很合适。如果值变化要更新界面，应该用 state。

```tsx
function useLatest<T>(value: T) {
  const ref = React.useRef(value)

  React.useEffect(() => {
    ref.current = value
  }, [value])

  return ref
}
```

`useLatest` 常用于异步回调或事件监听中读取最新值。

## 自定义 Hook

自定义 Hook 是以 `use` 开头的函数，可以调用其他 Hook。它复用的是逻辑结构，不是共享同一份状态。

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

如果要共享同一份数据，需要 Context、外部 store、查询缓存或服务端数据源。

## 闭包与依赖

Hooks 中最常见的问题是闭包旧值。每次渲染都有自己的 props、state 和函数，effect 或回调捕获的是那一次渲染的值。

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

这里使用函数式更新，不依赖定时器回调闭包里的旧 `count`。另一种方案是把最新值写入 ref。

## React 中 CSS 引入方式

React 不限制样式方案。常见方式包括普通 CSS、内联样式、CSS Modules、预处理器、CSS-in-JS、原子化 CSS 和组件库主题。

| 方式 | 特点 | 场景 |
| --- | --- | --- |
| 普通 CSS | 简单直接，但全局命名容易冲突 | 小项目、全局基础样式 |
| 内联样式 | 与组件同文件，动态方便，不支持伪类媒体查询 | 少量动态样式 |
| CSS Modules | 类名局部化，构建工具支持 | 组件级样式 |
| Sass/Less | 变量、嵌套、mixin | 传统工程样式体系 |
| CSS-in-JS | 样式和状态强绑定 | 主题、多租户、组件库 |
| 原子化 CSS | 组合类名快速构建 UI | 设计系统约束明确的项目 |

```tsx
import styles from './UserCard.module.css'

export function UserCard({ name }: { name: string }) {
  return <article className={styles.card}>{name}</article>
}
```

内联样式适合计算型场景：

```tsx
function ProgressBar({ percent }: { percent: number }) {
  return (
    <div
      style={{
        width: `${percent}%`,
        height: 8,
        backgroundColor: percent > 80 ? 'green' : 'orange'
      }}
    />
  )
}
```

团队选择样式方案时，应考虑作用域、主题能力、构建成本、服务端渲染、运行时开销和协作习惯。

## React 组件过渡动画

组件过渡动画的核心问题是：进入和退出都需要时间，而 React 条件渲染会直接挂载或卸载节点。要实现离场动画，通常需要额外的“可见状态”和“是否仍挂载”的状态。

```tsx
function FadePanel({ open }: { open: boolean }) {
  const [mounted, setMounted] = React.useState(open)

  React.useEffect(() => {
    if (open) {
      setMounted(true)
    }
  }, [open])

  if (!mounted) {
    return null
  }

  return (
    <section
      className={open ? 'fade-enter' : 'fade-exit'}
      onAnimationEnd={() => {
        if (!open) {
          setMounted(false)
        }
      }}
    >
      内容
    </section>
  )
}
```

对应 CSS 可以这样写：

```css
.fade-enter {
  animation: fade-in 160ms ease-out forwards;
}

.fade-exit {
  animation: fade-out 160ms ease-in forwards;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-out {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(4px); }
}
```

项目中也可以使用成熟库，例如基于进入、退出状态管理的过渡组件。无论使用哪种方式，都要处理动画结束回调、快速开关、卸载清理和无障碍焦点。

## Hooks、样式与动画检查清单

| 主题 | 建议 |
| --- | --- |
| Hook 调用 | 只在函数组件或自定义 Hook 顶层调用 |
| 状态更新 | 依赖旧值时使用函数式更新 |
| effect | 依赖数组真实完整，并提供必要清理 |
| layout effect | 只用于绘制前必须同步完成的 DOM 读写 |
| 缓存 | `useMemo` 和 `useCallback` 先定位问题再使用 |
| ref | 保存 DOM、实例或跨渲染可变值，不替代 state |
| CSS | 根据作用域、主题、SSR 和团队规范选择 |
| 动画 | 进入和退出状态分离，避免直接卸载导致离场动画丢失 |

