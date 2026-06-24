---
title: "React Notes: React + TS"
description: "React.md source note section: React + TS."
outline: [2, 3]
---

## react\+ts

### 创建项目

```JavaScript
pnpm create vite my-react-app --template react-ts
```

### useState添加泛型参数

```typescript
// react + ts

import { useState } from 'react'

type User = {
  name: string
  age: number
}

function App() {
  // 1. 限制初始值的类型
  // const [user, setUser] = useState<User>({
  //   name: 'jack',
  //   age: 18,
  // })
  // const [user, setUser] = useState<User>(() => {
  //   return {
  //     name: 'jack',
  //     age: 18,
  //   }
  // })

  const [user, setUser] = useState<User>({
    name: 'jack',
    age: 18,
  })

  const changeUser = () => {
    setUser(() => ({
      name: 'john',
      age: 28,
    }))
  }

  return <>this is app {user.name}</>
}

export default App

```

### useState赋初始值为null（用“\|”实现）

```typescript
// react + ts

import { useState } from 'react'

type User = {
  name: string
  age: number
}

function App() {
  const [user, setUser] = useState<User | null>(null)

  const changeUser = () => {
    setUser(null)
    setUser({
      name: 'jack',
      age: 18,
    })
  }
  // 为了类型安全  可选链做类型守卫
  // 只有user不为null（不为空值）的时候才进行点运算
  return <>this is app {user?.age}</>
}

export default App

```

### Props \+ ts基础

```typescript
// props + ts

// type Props = {
//   className: string
// }

interface Props {
  className: string // 必须传入
  title?: string  // 可选
}

function Button(props: Props) {
  const { className } = props
  return <button className={className}>click me </button>
}

function App() {
  return (
    <>
      <Button className="test" title="this is title" />
    </>
  )
}

export default App

```

### Props \+ ts中的children

```javascript
// props + ts

type Props = {
  className: string
  children: React.ReactNode
}

function Button(props: Props) {
  const { className, children } = props
  return <button className={className}>{children} </button>
}

function App() {
  return (
    <>
      <Button className="test">click me!</Button>
      <Button className="test">
        <span>this is span</span>
      </Button>
    </>
  )
}

export default App

```

### Props \+ ts中的事件

```typescript
// props + ts

type Props = {
  onGetMsg?: (msg: string) => void
}

function Son(props: Props) {
  const { onGetMsg } = props
  const clickHandler = () => {
    onGetMsg?.('this is msg')
  }
  return <button onClick={clickHandler}>sendMsg</button>
}

function App() {
  const getMsgHandler = (msg: string) => {
    console.log(msg)
  }
  return (
    <>
      <Son onGetMsg={(msg) => console.log(msg)} />
      <Son onGetMsg={getMsgHandler} />
    </>
  )
}

export default App

```

### useRef\+ts

```javascript
// useRef + ts

import { useEffect, useRef } from 'react'

// 1. 获取dom
// 2. 稳定引用的存储器（定时器管理）

function App() {
  const domRef = useRef<HTMLInputElement>(null)

  const timerId = useRef<number | undefined>(undefined)

  useEffect(() => {
    // 可选链  前面不为空值（null / undefined）执行点运算
    // 类型守卫 防止出现空值点运算错误
    domRef.current?.focus()

    timerId.current = setInterval(() => {
      console.log('123')
    }, 1000)

    return () => clearInterval(timerId.current)
  }, [])

  return (
    <>
      <input ref={domRef} />
    </>
  )
}

export default App

```

### ts\+接口封装

```typescript
import { http } from '@/utils'
// 接口响应数据通用
export type ResType<T> = {
  message: string
  data: T
}
//  2. 定义具体的接口类型

export type ChannelItem = {
  id: number
  name: string
}

type ChannelRes = {
  channels: ChannelItem[]
}

// 请求频道列表

export function fetchChannelAPI() {
  return http.request<ResType<ChannelRes>>({
    url: '/channels',
  })
}

// 请求文章列表

type ListItem = {
  art_id: string
  title: string
  aut_id: string
  comm_count: number
  pubdate: string
  aut_name: string
  is_top: number
  cover: {
    type: number
    images: string[]
  }
}

export type ListRes = {
  results: ListItem[]
  pre_timestamp: string
}

type ReqParams = {
  channel_id: string
  timestamp: string
}

export function fetchListAPI(params: ReqParams) {
  return http.request<ResType<ListRes>>({
    url: '/articles',
    params,
  })
}

```

### 类型出现错误

如果报错：

![Image](/images/react-notes/image-02.png)

解决（赋默认值，就不会为undefined）：

![Image](/images/react-notes/image-03.png)
