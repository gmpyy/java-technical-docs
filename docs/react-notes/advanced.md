---
title: "React Notes: React Advanced"
description: "React.md source note section: React Advanced."
outline: [2, 3]
---

## react高级

### useReducer（usestate高级版）

```javascript
// useReducer

import { useReducer } from "react"

// 1. 定义reducer函数 根据不同的action 返回不同的状态

function reducer (state, action) {
  switch (action.type) {
    case 'INC':
      return state + 1
    case 'DEC':
      return state - 1
    case 'SET':
      return action.payload
    default:
      return state
  }
}

// 2. 组件中调用useReducer(reducer, 0) => [state, dispatch]

// 3. 调用dispatch({type:'INC'}) => 通知reducer产生一个新的状态 使用这个新状态更新UI

function App () {
  const [state, dispatch] = useReducer(reducer, 0)
  return (
    <div className="App">
      this is app
      <button onClick={() => dispatch({ type: 'DEC' })}>-</button>
      {state}
      <button onClick={() => dispatch({ type: 'INC' })}>+</button>
      <button onClick={() => dispatch({ type: 'SET', payload: 100 })}>update</button>
    </div>
  )
}

export default App

```

### useImmer（替代usestate和usereducer）

```JavaScript
// usestate写法
setUser(prev => ({
  ...prev,
  profile: {
    ...prev.profile,
    name: 'Tom',
  },
}))

// useimmer写法
updateUser(draft => {
  draft.profile.name = 'Tom'
})
```

- useState 适合简单状态

- useImmer 适合“状态结构复杂，但状态管理逻辑本身不复杂”的场景

```JavaScript
// **useReducer**
function reducer(state, action) {
  switch (action.type) {
    case 'rename':
      return {
        ...state,
        profile: {
          ...state.profile,
          name: action.name,
        },
      }
    default:
      return state
  }
}

// useImmerReducer 
function reducer(draft, action) {
  switch (action.type) {
    case 'rename':
      draft.profile.name = action.name
      break
  }
}
```

- useReducer 适合“状态变化规则复杂”

- useImmerReducer 适合“状态变化规则复杂，而且 state 结构也复杂”

### useSyncExternalStore 

对于react内部的状态，比如使用了usestate这个hook，他会知道状态变了而重新渲染，但是对于一些外部的状态，例如：

- Redux、Zustand、自己手写的 store

- window / navigator 这类浏览器状态

- localStorage

- WebSocket 推送后的内存缓存

他不知道这些状态有没有变，需不需要重新渲染，因此提出了useSyncExternalStore ，它的核心目标只有一句话：**让 React 在渲染时拿到一份一致的外部状态快照，并在外部状态变化时正确重渲染。**

```JavaScript
const value = useSyncExternalStore(
  subscribe,//告诉react什么情况下快照会变
  getSnapshot,//当前快照
  getServerSnapshot?//服务端渲染的快照，在客户端渲染的时候可以不传
)
```

useSyncExternalStore 就是 React 提供给“外部状态订阅”的官方桥梁：

- subscribe 负责通知 React“外部状态变了”

- getSnapshot 负责告诉 React“现在的值是什么”

- 最大注意点是：**快照必须稳定，没变就返回同一个引用，否则很容易无限重渲染**

### **useTransition **

用于性能优化** 把“不需要立刻完成”的 state 更新降级，让 React 优先保证交互流畅。**

比较适合：

- 搜索筛选大列表

- 切换重 tab / 重页面

- 切换排序、筛选、视图模式后要渲染很多内容

- 路由切换时希望旧界面先保持稳定

不太适合：

- 简单组件状态

- 表单输入本身

- 很轻量、几乎无成本的更新

- 想拿它替代真正的性能优化

搜索筛选大表单就是快速输入多个字母，然后根据输入的内容更新表单，正常情况下每次输入都会去进行更新，但是使用useTransition优化之后，只有最后一次才会更新，前面的更新都被阻断了。

### **useDeferredValue **

用于性能优化，类似于防抖

**可以用这个判断法快速决定要不要上 useDeferredValue：**

- 用户当前操作是不是必须立刻反馈？

- 依赖这个值的某块 UI 是不是明显偏重？

- 我是不是希望“当前输入先走，重内容后到”？

如果这三个答案基本都是“是”，那就很适合。

最典型的一句话例子就是：

**输入框立刻更新，搜索结果慢一点更新。**

### **useLayoutEffect **

**useLayoutEffect 适合“需要在浏览器绘制前，先读 DOM、改 DOM、修正布局，避免用户看到闪一下”的场景。**

最典型的就是：

- tooltip / popover 定位

- 滚动位置修正

- 动画前测量布局

- 初始化依赖尺寸的 DOM 库

和useEffect的区别就是useEffect是异步，而**useLayoutEffect 是同步的，他会阻塞dom渲染。**

### useId

useId 的核心作用很简单：

**给当前组件实例生成一个稳定且唯一的 ID，主要用于把一组相关 DOM 元素关联起来，尤其是无障碍属性。**

**useId 不是用来标识“数据”的，而是用来标识“DOM 关系”的。**

最典型的就是：

- label 对应哪个 input

- input 由哪个提示文本描述

- 一组无障碍属性如何关联起来



### useMemo\(缓存\)

在一个组件中任意一个usestate的set方法被调用了，都会导致整个组件重新渲染，组件内部的代码也会重新执行。

利用useMemo可以将某个值缓存下来，其他无关的state变化的时候不会重新计算

```javascript
// useMemo
// 缓存: 消耗非常大的计算

import { useMemo, useState } from "react"

// 计算斐波那契数列之和
function fib (n) {
  console.log('计算函数执行了')
  if (n < 3)
    return 1
  return fib(n - 2) + fib(n - 1)
}

function App () {
  const [count1, setCount1] = useState(0)

  const result = useMemo(() => {
    // 返回计算得到的结果
    return fib(count1)
  }, [count1])

  // const result = fib(count1)

  const [count2, setCount2] = useState(0)
  console.log('组件重新渲染了')
  return (
    <div className="App">
      this is app
      <button onClick={() => setCount1(count1 + 1)}>change count1: {count1}</button>
      <button onClick={() => setCount2(count2 + 1)}>change count2: {count2}</button>
      {result}
    </div>
  )
}

export default App

```

### react\.memo\(子组件的缓存\)

```javascript
// React.memo

import { memo, useState } from "react"

// 1. 验证默认的渲染机制  子跟着父一起渲染

// 2. memo进行缓存  只有props发生变化的时候才会重新渲染 （不考虑context）

const MemoSon = memo(function Son () {
  console.log('我是子组件，我重新渲染了')
  return <div>this is son</div>
})

// function Son () {
//   console.log('我是子组件，我重新渲染了')
//   return <div>this is son</div>
// }

function App () {
  const [count, setCount] = useState(0)
  return (
    <div className="App">
      <button onClick={() => setCount(count + 1)}>+{count}</button>
      {/* <Son /> */}
      <MemoSon />
    </div>
  )
}

export default App

```

### react\.memo中props的比较机制

```javascript
// React.memo props比较机制

// 1. 传递一个简单类型的prop   prop变化时组件重新渲染

// 2. 传递一个引用类型的prop   比较的是新值和旧值的引用是否相等  当父组件的函数重新执行时，实际上形成的是新的数组引用

// 3. 保证引用稳定 -> useMemo 组件渲染的过程中缓存一个值

import { memo, useMemo, useState } from 'react'

const MemoSon = memo(function Son ({ list }) {
  console.log('子组件重新渲染了')
  return <div>this is Son {list}</div>
})

function App () {
  const [count, setCount] = useState(0)

  // const num = 100

  const list = useMemo(() => {
    return [1, 2, 3]
  }, [])

  return (
    <div className="App">
      <MemoSon list={list} />
      <button onClick={() => setCount(count + 1)}>change Count</button>
    </div>
  )
}

export default App

```

### usecallback\(类似useMemo，只不过缓存的是一个函数\)

```javascript
// useCallback

import { memo, useCallback, useState } from "react"

const Input = memo(function Input ({ onChange }) {
  console.log('子组件重新渲染了')
  return <input type="text" onChange={(e) => onChange(e.target.value)} />
})

function App () {
  // 传给子组件的函数
  const changeHandler = useCallback((value) => console.log(value), [])
  // 触发父组件重新渲染的函数
  const [count, setCount] = useState(0)
  return (
    <div className="App">
      {/* 把函数作为prop传给子组件 */}
      <Input onChange={changeHandler} />
      <button onClick={() => setCount(count + 1)}>{count}</button>
    </div>
  )
}

export default App

```

### forwardRef

父组件想要获取子组件内部的某个元素，就要使用forwardRef，所以forwardRef绑定的是一个组件。

不同于ref直接绑定的是一个dom元素

```javascript
import { forwardRef, useRef } from "react"

// 子组件
// function Son () {
//   return <input type="text" />
// }

const Son = forwardRef((props, ref) => {
  return <input type="text" ref={ref} />
})

// 父组件
function App () {
  const sonRef = useRef(null)
  const showRef = () => {
    console.log(sonRef)
    sonRef.current.focus()
  }
  return (
    <>
      <Son ref={sonRef} />
      <button onClick={showRef}>focus</button>
    </>
  )
}

export default App
```

### useInperativeHandle\(父组件调用子组件内部的方法\)

```javascript
import { forwardRef, useImperativeHandle, useRef } from "react"

// 子组件

const Son = forwardRef((props, ref) => {
  // 实现聚焦逻辑
  const inputRef = useRef(null)
  const focusHandler = () => {
    inputRef.current.focus()
  }

  // 把聚焦方法暴露出去
  useImperativeHandle(ref, () => {
    return {
      // 暴露的方法
      focusHandler
    }
  })
  return <input type="text" ref={inputRef} />
})

// 父组件
function App () {
  const sonRef = useRef(null)
  const focusHandler = () => {
    console.log(sonRef.current)
    sonRef.current.focusHandler()
  }
  return (
    <>
      <Son ref={sonRef} />
      <button onClick={focusHandler}>focus</button>
    </>
  )
}

export default App
```

### CLASS API基础结构

```javascript
// Class API

import { Component } from "react"

class Counter extends Component {
  // 编写组件的逻辑代码
  // 1. 状态变量  2. 事件回调  3.UI(JSX)
  // 1. 定义状态变量
  state = {
    count: 0
  }

  // 2. 定义事件回调修改状态数据
  setCount = () => {
    // 修改状态数据
    this.setState({
      count: this.state.count + 1
    })
  }

  render () {
    return <button onClick={this.setCount}>{this.state.count}</button>
  }
}

function App () {
  return (
    <>
      <Counter />
    </>
  )
}

export default App
```

### CLASS API中组件生命周期

```javascript
// Class API 生命周期

import { Component, useState } from "react"

class Son extends Component {
  // 声明周期函数
  // 组件渲染完毕执行一次  发送网络请求
  componentDidMount () {
    console.log('组件渲染完毕了，请求发送起来')
    // 开启定时器
    this.timer = setInterval(() => {
      console.log('定时器运行中')
    }, 1000)
  }

  // 组件卸载的时候自动执行  副作用清理的工作 清除定时器 清除事件绑定
  componentWillUnmount () {
    console.log('组件son被卸载了')
    // 清除定时器
    clearInterval(this.timer)
  }

  render () {
    return <div>i am Son</div>
  }
}

function App () {
  const [show, setShow] = useState(true)
  return (
    <>
      {show && <Son />}
      <button onClick={() => setShow(false)}>unmount</button>
    </>
  )
}

export default App
```
