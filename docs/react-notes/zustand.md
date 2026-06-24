---
title: "React Notes: Zustand"
description: "React.md source note section: Zustand."
outline: [2, 3]
---

## 状态管理工具zustand

### 基本使用

```javascript
// zustand
import { create } from 'zustand'

// 1. 创建store
// 语法容易出错
// 1. 函数参数必须返回一个对象 对象内部编写状态数据和方法
// 2. set是用来修改数据的专门方法必须调用它来修改数据
// 语法1：参数是函数 需要用到老数据的场景   
// 语法2：参数直接是一个对象  set({ count: 100 })

const useStore = create((set) => {
  return {
    // 状态数据
    count: 0,
    // 修改状态数据的方法
    inc: () => {
      set((state) => ({ count: state.count + 1 }))
    }
  }
})

// 2. 绑定store到组件
// useStore => { count, inc }

function App () {
  const { count, inc } = useStore()
  return (
    <>
      <button onClick={inc}>{count}</button>
    </>
  )
}

export default App
```

### 处理异步操作

```javascript
// zustand
import { useEffect } from 'react'
import { create } from 'zustand'
const URL = 'http://geek.itheima.net/v1_0/channels'

// 1. 创建store
// 语法容易出错
// 1. 函数参数必须返回一个对象 对象内部编写状态数据和方法
// 2. set是用来修改数据的专门方法必须调用它来修改数据
// 语法1：参数是函数 需要用到老数据的场景   
// 语法2：参数直接是一个对象  set({ count: 100 })

const useStore = create((set) => {
  return {
    // 状态数据
    count: 0,
    // 修改状态数据的方法
    inc: () => {
      set((state) => ({ count: state.count + 1 }))
    },
    channelList: [],
    fetchGetList: async () => {
      const res = await fetch(URL)
      const jsonRes = await res.json()
      console.log(jsonRes)
      set({
        channelList: jsonRes.data.channels
      })
    }
  }
})

// 2. 绑定store到组件
// useStore => { count, inc }

function App () {
  const { count, inc, fetchGetList, channelList } = useStore()
  useEffect(() => {
    fetchGetList()
  }, [fetchGetList])
  return (
    <>
      <button onClick={inc}>{count}</button>
      <ul>
        {
          channelList.map(item => <li key={item.id}>{item.name}</li>)
        }
      </ul>
    </>
  )
}

export default App
```

### 切片模式

```javascript
// zustand
import { useEffect } from 'react'
import { create } from 'zustand'
const URL = 'http://geek.itheima.net/v1_0/channels'

// store
// counterStore  
// channelStore 
// index.js

// 1. 拆分子模块 再组合起来

const createCounterStore = (set) => {
  return {
    // 状态数据
    count: 0,
    // 修改状态数据的方法
    inc: () => {
      set((state) => ({ count: state.count + 1 }))
    },
  }
}

const createChannelStore = (set) => {
  return {
    channelList: [],
    fetchGetList: async () => {
      const res = await fetch(URL)
      const jsonRes = await res.json()
      console.log(jsonRes)
      set({
        channelList: jsonRes.data.channels
      })
    }
  }
}

const useStore = create((...a) => {
  return {
    ...createCounterStore(...a),
    ...createChannelStore(...a)
  }
})

function App () {
  // 2. 组件使用
  const { count, inc, fetchGetList, channelList } = useStore()
  useEffect(() => {
    fetchGetList()
  }, [fetchGetList])
  return (
    <>
      <button onClick={inc}>{count}</button>
      <ul>
        {
          channelList.map(item => <li key={item.id}>{item.name}</li>)
        }
      </ul>
    </>
  )
}

export default App
```
