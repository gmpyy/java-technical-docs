---
title: "React Notes: React Basics"
description: "React.md source note section: React Basics."
outline: [2, 3]
---

# React

https://nextjs\-docs\-henna\-six\.vercel\.app/tutorials/server\-actions

https://message163\.github\.io/react\-docs/react/basic/introduce\.html



### 使用脚手架创建react项目

```JavaScript
//全局安装脚手架
npm i create-react-app -g
//检查安装情况
create-react-app --version
//基于脚手架创建项目
create-react-app 项目名称
```

### 项目文件清理

src目录下只保留app\.js和index\.js

```JavaScript
//app.js
// 项目的根组件
function App() {
  return (
    <div className="App">
      this is react
    </div>
  );
}

export default App;

//index.js
// 整个项目运行的入口
// 1.导入核心包
import React from 'react';
import ReactDOM from 'react-dom/client';
// 2.导入根组件
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

```

### jsx表达式

```java
// 项目的根组件
const count = 100
function getname(){
  return 'jeck'
}
function App() {
  return (
    <div className="App">
      this is react
      {/* {使用引号传递字符串} */}
      {'this is message'}
      {/* {识别js变量} */}
      {count}
      {/* {函数调用} */}
      {getname()}
      {/* {方法调用} */}
      {new Date().getTime()}
      {/* {使用js对象} */}
      <div style={{color:'red'}}>this is div</div>
    </div>
  );
}

export default App;

```

### react中的for循环渲染列表

```javascript
// 项目的根组件
const list = [
  {id:1001,name:'vue'},
  {id:1001,name:'react'},
  {id:1001,name:'angular'}
]

function App() {
  return (
    <div className="App">
      {/* {渲染列表} */}
      {/* {注意事项：加上一个独一无二的key，可以是字符串，也可以是number} */}
     <ul>
      {list.map((item)=><li key={item.id}>{item.name}</li>)}
     </ul>
    </div>
  );
}

export default App;

```

### react中的条件渲染

```javascript
// 项目的根组件
let isLogin = false
const list = [
  {id:1001,type:1},
  {id:1002,type:2},
  {id:1003,type:3},
]
function getArticleTem(item){
  if(item.type === 1){
    return <div key={item.id}>无图文章</div>
  }else if(item.type === 2){
    return <div key={item.id}>单图文章</div>
  }else{
    return <div key={item.id}>三图文章</div>
  }
}
function App() {
  return (
    <div className="App">
      {/* {&&控制显示隐藏} */}
     {isLogin && <span>this is span</span>}
     {isLogin ? <span>jack</span> : <span>loading...</span>}
     <ul>
      {list.map((item)=>getArticleTem(item))}
     </ul>
    </div>
  );
}

export default App;

```

### react中的事件监听

```javascript
// 项目的根组件
// 注意事件监听的大括号里面是一个函数，不同于函数调用大括号里面是函数执行
const handleClick = (name,e) => {
  console.log('button被点击了',name,e)
}
function App() {
  return (
    <div className="App">
     <button onClick={(e)=>handleClick('jack',e)}>点击我</button>
    </div>
  );
}

export default App;

```

### react中组件的基本使用

```javascript
// 项目的根组件
const Button = () => {
  return <button>click me</button>
}
function App() {
  return (
    <div className="App">
     <Button></Button>
    </div>
  );
}

export default App;

```

### react中的视图和数据实时更新useState

```javascript
// 项目的根组件

import { useState } from "react"
function App() {
  // count 状态变量
  // setState 修改状态变量的方法
  const [count, setCount] = useState({
    name: 'jack'
  })
  const handleClick = () => {
    count.name = 'john'
    //修改值一定要调用set方法
    setCount({
      ...count
    })
  }
  return (
    <div className="App">
      <button onClick={handleClick}>click me {count.name}</button>
    </div>
  );
}

export default App;

```

### react中的计算属性useMemo

```JavaScript
import { useMemo } from 'react'
// 第二个参数是一个数组，表示计算依赖的数据，依赖的数据如果发生变化会重新计算
const Month = useMemo(()=>{
    return billList
},[billList])
```

### 基础样式控制

```javascript
// 项目的根组件
import './index.css'
const style = {
  color:'blue',
  fontSize: '50px'
}
function App() {
  
  return (
    <div className="App">
      <span style={style}>this is a span</span>
      <br />
      <span className='foo'>this is a span2</span>
    </div>
  );
}

export default App;

```

### classname库控制类名

![Image](/images/react-notes/image-01.png)

### 表单的受控绑定

```javascript
// 项目的根组件
import { useState } from "react"

function App() {
  const [value, setValue] = useState('')
  return (
    <div className="App">
      <input
        value={value}
        onChange={(e)=>setValue(e.target.value)}
        type="text"
      ></input>
    </div>
  );
}

export default App;

```

### 获取DOM元素

```JavaScript
1.使用useRef创建ref对象，并且绑定
const inputRef = useRef(null)
<input type="text" ref={inputRef} />
2.在DOM可用的时候通过inputRef.current拿到DOM


// 项目的根组件
import { useRef } from "react"

function App() {
  const inputRef = useRef(null)
  const showDom = () => {
    console.log(inputRef.current)
  }
  return (
    <div className="App">
      <input type="text" ref={inputRef}></input>
      <button onClick={showDom}>获取dom</button>
    </div>
  );
}

export default App;

```

### 父子通信之父传子

```javascript
// 项目的根组件
// 父传子
// 1.父组件传递数据 子组件标签身上绑定属性
// 2.子组件接收数据用props
// 注意props只读

function Son (props) {
  console.log(props)
  return <div>this is Son, {props.name}</div>
}
function App() {
  const name= 'jack'
  return (
    <div className="App">
      <Son name={name}></Son>
    </div>
  );
}

export default App;
```

### 父传子中props的children属性

```javascript
// 项目的根组件
// 父传子
// props的children属性其实就是嵌套在子组件标签里面的内容（标签）

function Son (props) {
  console.log(props)
  return <div>this is Son, {props.name}<br/>{props.children}</div>
}
function App() {
  const name= 'jack'
  return (
    <div className="App">
      <Son name={name}>
        <span>this is a span</span>
      </Son>
    </div>
  );
}

export default App;

```

### 子传父

```javascript
// 项目的根组件
// 子传父
import { useState } from "react";
function Son (props) {
  // Son组件中的数据
  const sonMsg = 'this is son msg'
  return (<div>
    this is Son
    <button onClick={()=>props.onGetSonMsg(sonMsg)}>sendMsg</button>
  </div>)
}
function App() {
  const [msg, setMsg] = useState('')
  const getMsg = (msg) => {
    console.log(msg)
    setMsg(msg)
  }
  return (
    <div className="App">
      this is App, {msg}
      <Son onGetSonMsg={getMsg}>
      </Son>
    </div>
  );
}

export default App;

```

### 兄弟组件通信

```javascript
// 项目的根组件
// 兄弟组件通信
// 1.子传父将a组件数据传到app
// 2.父传子将app数据再传到b
import { useState } from "react";
function A ({ onGetName }){
  const name = 'this is A name'
  return (
    <div>
      this is A component,
      <button onClick={()=>onGetName(name)}>send</button>
    </div>
  )
}
function B ({ name }){
  return (
    <div>
      this is B component,
      {name}
    </div>
  )
}
function App() {
  const [msg, setMsg] = useState('')
  const getMsg = (msg) => {
    console.log(msg)
    setMsg(msg)
  }
  return (
    <div className="App">
      <A onGetName={getMsg}></A>
      <B name={msg}></B>
    </div>
  );
}

export default App;

```

### 兄弟组件通信之new Event

```JavaScript
// eventBus.ts
export const orderBus = new EventTarget()

// OrderToolbar.tsx
import { orderBus } from './eventBus'

export default function OrderToolbar() {
  return (
    <button
      onClick={() => {
        orderBus.dispatchEvent(new Event('orders:refresh'))
      }}
    >
      刷新订单
    </button>
  )
}

// OrderList.tsx
import { useEffect, useState } from 'react'
import { orderBus } from './eventBus'

type Order = {
  id: number
  title: string
}

export default function OrderList() {
  const [orders, setOrders] = useState<Order[]>([])

  async function loadOrders() {
    const data = await Promise.resolve([
      { id: 1, title: '订单 A' },
      { id: 2, title: '订单 B' },
    ])
    setOrders(data)
  }

  useEffect(() => {
    loadOrders()

    const handleRefresh = () => {
      loadOrders()
    }

    orderBus.addEventListener('orders:refresh', handleRefresh)

    return () => {
      orderBus.removeEventListener('orders:refresh', handleRefresh)
    }
  }, [])

  return (
    <ul>
      {orders.map((item) => (
        <li key={item.id}>{item.title}</li>
      ))}
    </ul>
  )
}
```

### 兄弟组件通信之mitt

```TypeScript
// commentBus.ts
import mitt from 'mitt'

type CommentItem = {
  id: string
  author: string
  content: string
  createdAt: string
}

type Events = {
  'comment:created': CommentItem
}

export const commentBus = mitt<Events>()

// CommentEditor.tsx
import { useState } from 'react'
import { commentBus } from './commentBus'

export default function CommentEditor() {
  const [content, setContent] = useState('')

  async function handleSubmit() {
    if (!content.trim()) return

    const newComment = {
      id: String(Date.now()),
      author: '张三',
      content,
      createdAt: new Date().toLocaleString(),
    }

    // 模拟接口成功后广播事件
    commentBus.emit('comment:created', newComment)
    setContent('')
  }

  return (
    <div>
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="写点评论..."
      />
      <button onClick={handleSubmit}>发布评论</button>
    </div>
  )
}

// CommentList.tsx
import { useEffect, useState } from 'react'
import { commentBus } from './commentBus'

type CommentItem = {
  id: string
  author: string
  content: string
  createdAt: string
}

export default function CommentList() {
  const [comments, setComments] = useState<CommentItem[]>([
    {
      id: '1',
      author: '李四',
      content: '第一条评论',
      createdAt: '2026/04/07 10:00:00',
    },
  ])

  useEffect(() => {
    const handleCreated = (newComment: CommentItem) => {
      setComments((prev) => [newComment, ...prev])
    }

    commentBus.on('comment:created', handleCreated)

    return () => {
      commentBus.off('comment:created', handleCreated)
    }
  }, [])

  return (
    <ul>
      {comments.map((item) => (
        <li key={item.id}>
          <strong>{item.author}</strong>：{item.content}
        </li>
      ))}
    </ul>
  )
}
```

### 父传孙

```javascript
// 项目的根组件
// 爷传孙
import { createContext, useContext } from 'react'
// 1.createContext方法创建一个上下文对象
const MsgContext = createContext()
//2.在顶层组件通过Provider组件提供数据

// 3. 在底层组件 通过useContext钩子函数使用数据
function A (){
  return (
    <div>
      this is A component,
      <B></B>
    </div>
  )
}
function B (){
  const msg = useContext(MsgContext)
  return (
    <div>
      this is B component,{msg}
    </div>
  )
}
function App() {
  const msg = 'this is app msg'
  return (
    <div className="App">
     <MsgContext.Provider value={msg}>
      this is App
      <A></A>
     </MsgContext.Provider>
    </div>
  );
}

export default App;

```

### useEffect的使用（包含依赖项说明）

```javascript
// 项目的根组件
// 利用useEffect实现组件渲染完成后执行操作（比如发送请求）
import { useEffect, useState } from "react";
function App() {
  const [list, setList] = useState([])
  //第二个参数是依赖项，依赖项为空数组的时候只执行一次
  useEffect(()=>{
    async function getList () {
      const res = await fetch('http://geek.itheima.net/v1_0/channels')
      const jsonRes = await res.json()
      setList(jsonRes.data.channels)
    }
    getList()
  },[])
  return (
    <div className="App">
     <ul>
      {list.map((item)=><li key={item.id}>{item.name}</li>)}
     </ul>
    </div>
  );
}

export default App;

```

依赖项：

1\.没有依赖项的时候执行时机

- 组件初始化渲染

- 组件更新（也就是某个state变化就会执行）

2\.依赖项是空数组

- 组件初始化渲染

3\.添加特定依赖项

- 组件初始化渲染

- 特定依赖项变化（特定的state变化）

```javascript
// 项目的根组件
// 利用useEffect实现组件渲染完成后执行操作（比如发送请求）
import { useEffect, useState } from "react";
function App() {
  const [count, setCount] = useState(0)
  // 传入特定依赖项
  useEffect(()=>{
    console.log('特定依赖项发生了变化')
  },[count])
  return (
    <div className="App">
     <button onClick={()=>setCount(count + 1)}>{count}</button>
    </div>
  );
}

export default App;

```

依赖项的清除副作用（组件被卸载的时候就会触发）

比如在useEffect中开启一个定时器，我们想要在组件卸载时清理掉定时器

```JavaScript
useEffect(()=>{
    return ()=>{
        //清除副作用
    }
},[])
```

```javascript
// 项目的根组件
import { useEffect, useState } from "react";

function Son () {
  useEffect(()=>{
    const timer = setInterval(()=>{
      console.log('定时器执行中。。。')
    },1000)
    return ()=>{
      clearInterval(timer)
    }
  },[])
  return <div>this is son</div>
}
function App() {
  const [count, setCount] = useState(true)
  
  return (
    <div className="App">
     {count && <Son></Son>}
     <button onClick={()=>setCount(false)}>卸载son组件</button>
    </div>
  );
}

export default App;
```

### 自定义hook实现代码逻辑复用

```javascript
// 项目的根组件
//自定义hook实现逻辑代码复用
// 1.声明一个以use开头的函数
// 2.在函数体内封装可复用逻辑
// 3.把组件中用到的状态或者函数return
// 4.在哪个组件中要用到这个逻辑，就执行这个函数，解构出来状态和函数直接使用
import { useState } from "react";

function useToggle () {
  // 可复用的代码
  const [value, setValue] = useState(true)

  const toggle = () => setValue(!value)

  return {
    value,
    toggle
  }
}
function App() {
  const {value, toggle} = useToggle()
  
  return (
    <div className="App">
     {value && <div>this is div</div>}
     <button onClick={toggle}>toggle</button>
    </div>
  );
}

export default App;

```

### hooks使用规则

1\.只能在组件内使用，不能在组件外使用

```JavaScript
// 会报错
const [value, setValue] = useState('')
function App () {
    return (
        <div>
            this is app
        </div>
    )
}
```

2\.只能在组件的顶层调用，不能嵌套在if，for，其他函数中

```JavaScript
function App () {
    if(Math.random() > 0.5){
        const [value, setValue] = useState('')
    }
    return (
        <div>
            this is app
        </div>
    )
}
```

### HOC高阶组件

#### 进阶用法

封装一个通用的HOC，实现埋点统计，比如点击事件，页面挂载，页面卸载等。

封装一个埋点服务可以根据自己的业务自行扩展

1. `trackType`表示发送埋点的组件类型

2. `data`表示发送的数据

3. `eventData`表示需要统计的用户行为数据

4. `navigator.sendBeacon`是浏览器提供的一种安全可靠的异步数据传输方式，适合发送少量数据，比如埋点数据,并且浏览器关闭时，数据也会发送，不会阻塞页面加载

```TypeScript
const trackService = {
  sendEvent: <T,>(trackType: string, data: T = null as T) => {
    const eventData = {
      timestamp: Date.now(), // 时间戳
      trackType, // 事件类型
      data, // 事件数据
      userAgent: navigator.userAgent, // 用户代理
      url: window.location.href, // 当前URL
    }
    //发送数据
    navigator.sendBeacon(
      'http://localhost:5173',
      JSON.stringify(eventData)
    )
  }
}
// 实现HOC高阶组件,通过useEffect统计组件挂载和卸载，并且封装一个trackEvent方法，传递给子组件，子组件可以自行调用，统计用户行为。
const withTrack = (Component: React.ComponentType<any>, trackType: string) => {
  return (props: any) => {
    useEffect(() => {
      //发送数据 组件挂载
      trackService.sendEvent(`${trackType}-MOUNT`)
      return () => {
        //发送数据 组件卸载
        trackService.sendEvent(`${trackType}-UNMOUNT`)
      }
    }, [])

    //处理事件
    const trackEvent = (eventType: string, data: any) => {
      trackService.sendEvent(`${trackType}-${eventType}`, data)
    }


    return <Component {...props} trackEvent={trackEvent} />
  }
}

// 使用HOC高阶组件,注册了一个button按钮，并传递了trackEvent方法，子组件可以自行调用，统计用户行为。
const Button = ({ trackEvent }) => {
  // 点击事件
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    trackEvent(e.type, {
      name: e.type,
      type: e.type,
      clientX: e.clientX,
      clientY: e.clientY,
    })
  }

  return <button   onClick={handleClick}>我是按钮</button>
}
// 使用HOC高阶组件
const TrackButton = withTrack(Button, 'button')
// 使用组件
const App = () => {
  return <div>
    <TrackButton />
  </div>
}

export default App
```

### createPortal传送api

入参

- children：要渲染的组件

- domNode：要渲染到的DOM位置

- key?：可选，用于唯一标识要渲染的组件

返回值

- 返回一个React元素\(即jsx\)，这个元素可以被React渲染到DOM的任意位置

使用场景：

- 弹窗

- 下拉框

- 全局提示

- 全局遮罩

- 全局Loading

全局弹窗示例，通过api让弹窗挂载到document\.body下面：

```JavaScript
import './index.css';
import { createPortal } from 'react-dom';
export const Modal = () => {
  return createPortal(<div className="modal">
    <div className="modal-header">
      <div className="modal-title">标题</div>
    </div>
    <div className="modal-content">
      <h1>Modal</h1>
    </div>
    <div className="modal-footer">
      <button className="modal-close-button">关闭</button>
        <button className="modal-confirm-button">确定</button>
      </div>
    </div>,
    document.body
  )
}
```
