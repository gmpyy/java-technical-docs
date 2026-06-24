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

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MzNhNDFlZDdmMDFlODljODg1NTk4MDUxOWE2MjkwZDNfNmI5ZTJlYmM5ODMwN2Q0MmMxODAyYTY4ZGQ2NzNmMDRfSUQ6NzUwMDIyNzE3NTcyMDY5Nzg2MF8xNzgyMzE5MDc5OjE3ODI0MDU0NzlfVjM)

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



## 状态管理工具Redux

### 创建react\+redux项目

```JavaScript
1.使用CRA快速创建React项目
create-react-app react-redux
2.安装配套工具
npm i @reduxjs/toolkit react-redux
3.启动项目
npm run start
```

实现计数器

```JavaScript
// ./store/modules/counterStore.js
import { createSlice } from "@reduxjs/toolkit";

const counterStore = createSlice({
  name: 'counter',
  // 初始状态数据
  initialState: {
    count:0
  },
  // 修改数据的同步方法
  reducers: {
    increment(state){
      state.count++
    },
    decrement (state){
      state.count--
    }
  }
})

// 解构出创建action对象的函数
const { increment, decrement } = counterStore.actions
// 获取reducer函数
const counterRender = counterStore.reducer
// 导出
export { increment, decrement }
export default counterRender
```

```javascript
// ./store/index.js
import { configureStore } from "@reduxjs/toolkit";
import counterReducer  from "./modules/counterStore";

// 创建根store组合子模块
const store = configureStore({
  reducer: {
    counter: counterReducer
  }
})

export default store
```

```JavaScript
// ./index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import store from './store'
import { Provider } from 'react-redux'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);

```

```JavaScript
// ./app.js
import { useDispatch, useSelector } from "react-redux";
// 导入actionCreater
import { increment, decrement } from './store/modules/counterStore'

function App() {
  const { count } = useSelector(state => state.counter)
  const dispatch = useDispatch()
  return (
    <div className="App">
      <button onClick={()=>dispatch(decrement())}>-</button>
      {count}
      <button onClick={()=>dispatch(increment())}>+</button>
    </div>
  );
}

export default App;

```

### redux中的action接收参数

```javascript
// ./store/modules/counterStore.js
import { createSlice } from "@reduxjs/toolkit";

const counterStore = createSlice({
  name: 'counter',
  // 初始状态数据
  initialState: {
    count:0
  },
  // 修改数据的同步方法
  reducers: {
    increment(state){
      state.count++
    },
    decrement (state){
      state.count--
    },
    addToNum(state,action){
      state.count += action.payload
    }
  }
})

// 解构出创建action对象的函数
const { increment, decrement, addToNum } = counterStore.actions
// 获取reducer函数
const counterRender = counterStore.reducer
// 导出
export { increment, decrement, addToNum }
export default counterRender
```

```JavaScript
// ./app.js
import { useDispatch, useSelector } from "react-redux";
// 导入actionCreater
import { increment, decrement, addToNum } from './store/modules/counterStore'

function App() {
  const { count } = useSelector(state => state.counter)
  const dispatch = useDispatch()
  return (
    <div className="App">
      <button onClick={()=>dispatch(decrement())}>-</button>
      {count}
      <button onClick={()=>dispatch(increment())}>+</button>
      <button onClick={()=>dispatch(addToNum(10))}>+10</button>
    </div>
  );
}

export default App;

```

### redux中处理异步操作

1\.创建store的写法保持不变，配置好同步修改状态的方法

2\.单独封装一个函数，在函数内部return一个新函数，在新函数中

2\.1封装异步请求获取数据

2\.2调用同步修改状态的方法，传入异步数据生成一个action对象，并且使用dispatch提交

```javascript
// ./store/modules/channelStore.js
import { createSlice } from "@reduxjs/toolkit";
import axios from "axios"

const channelStore = createSlice({
  name: 'channel',
  initialState: {
    channelList: []
  },
  // 修改数据的同步方法
  reducers: {
    setChannels(state,action) {
      state.channelList = action.payload
    }
  }
})

//异步请求

// 解构出创建action对象的函数
const { setChannels } = channelStore.actions

const fetchChannelList = () => {
  return async (dispatch) => {
    const res = await axios.get('http://geek.itheima.net/v1_0/channels')
    dispatch(setChannels(res.data.data.channels))
  }
}

export { fetchChannelList }
// 获取reducer函数
const channelReducer = channelStore.reducer

export default channelReducer
```

3\.组件中dispatch的写法保持不变

```javascript
import { useDispatch, useSelector } from "react-redux";
// 导入actionCreater
import { increment, decrement, addToNum } from './store/modules/counterStore'
import { useEffect } from "react";
import { fetchChannelList } from "./store/modules/channelStore";

function App() {
  const { count } = useSelector(state => state.counter)
  const { channelList } = useSelector(state => state.channel)
  const dispatch = useDispatch()
  useEffect(()=>{
    dispatch(fetchChannelList())
  },[dispatch])
  return (
    <div className="App">
      <button onClick={()=>dispatch(decrement())}>-</button>
      {count}
      <button onClick={()=>dispatch(increment())}>+</button>
      <button onClick={()=>dispatch(addToNum(10))}>+10</button>
      <ul>
        {channelList.map((item)=><li key={item.id}>{item.name}</li>)}
      </ul>
    </div>
  );
}

export default App;

```

## react路由

### 示例

```JavaScript
// 1.安装包
// npm i react-router-dom


// 2.在index.js中进行配置
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
// 1.导入两个模块
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
// 2.配置路由
const router = createBrowserRouter([
  {
    path:'/login',
    element:<div>我是登录页</div>
  },
  {
    path:'/article',
    element:<div>我是文章页</div>
  },
])
const root = ReactDOM.createRoot(document.getElementById('root'));
// 3.添加routerprovider标签
root.render(
  <React.StrictMode>
    <RouterProvider router={router}>
      <App />
    </RouterProvider>
  </React.StrictMode>
);

```

### 路由跳转方法

```javascript
import { Link, useNavigate } from 'react-router-dom'
const Login = () => {
  const navigate = useNavigate()
  return (
    <div>
      我是登录页
      {/* {声明式写法} */}
      <Link to="/article">点击跳转文章页</Link>
      {/* {命令式写法} */}
      <button onClick={()=>navigate('/article')}>点击跳转文章页</button>
    </div>
  )
}

export default Login
```

### 路由传参方法

```JavaScript
1.searchParams传参
// 传参
navigate('/article?id=1001&name=jack')
// 接收
import { useSearchParams } from 'react-router-dom'
const [params] = useSearchParams()
let id = params.get('id')

2.params传参
// 传参
// 配置路由的时候
{
    path:'/article/:id',
    element:<div>我是文章页</div>
},
// 传参时
navigate('/article/1001')
// 接收
import { useParams } from 'react-router-dom'
const params = useParams()
let id = params.id

3.state传参
/*
适用于：传递复杂数据结构
特点：支持任意类型数据，参数不显示在URL
限制：刷新可能丢失，不利于分享
选择建议：必要参数用 Params，筛选条件用 Query，临时数据用 State。
*/
```

### 嵌套路由实现步骤

```JavaScript
// 1.配置路由的时候使用children属性配置路由嵌套关系
{
    path:'/',
    element:<Layout />,
    children: [
        {
            path:'board',
            element:<Board />,
        },
        {
            path:'about',
            element:<About />,
        }
    ]
}

// 2.使用'<Outlet />'组件配置二级路由在一级路由页面渲染的位置
const Layout = () => {
    return (
        <div>我是Layout</div>
        
        {/* 二级路由出口 */}
        <Outlet />
    )
}
```

### 默认渲染二级路由的实现

比如说上面的例子，访问/的时候想要默认渲染board组件的内容，只需要

1. 在二级路由的位置去掉path

2. 设置index属性为true

```JavaScript
{
    path:'/',
    element:<Layout />,
    children: [
        {
            index:true,
            element:<Board />,
        },
        {
            path:'about',
            element:<About />,
        }
    ]
}
```

### 配置404页面

当用户输入一个不存在的path，将跳转到404页面，以下是404页面的路由配置

```javascript
const router = createBrowserRouter([
  {
    path:'/login',
    element:<div>我是登录页</div>
  },
  {
    path:'/article',
    element:<div>我是文章页</div>
  },
  // 注意404页面要放到路由的末尾
  {
    path:'*',
    element:<NotFound />
  },
])
```

### 切换哈希模式

```javascript
// 1.安装包
// npm i react-router-dom


// 2.在index.js中进行配置
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
// 1.导入两个模块
import { createBrowserRouter,createHashRouter, RouterProvider } from 'react-router-dom'
// 2.配置路由,切换哈希模式
const router = createHashRouter([
  {
    path:'/login',
    element:<div>我是登录页</div>
  },
  {
    path:'/article',
    element:<div>我是文章页</div>
  },
])
const root = ReactDOM.createRoot(document.getElementById('root'));
// 3.添加routerprovider标签
root.render(
  <React.StrictMode>
    <RouterProvider router={router}>
      <App />
    </RouterProvider>
  </React.StrictMode>
);

```

## 实际项目开发

### token鉴权实现

```JavaScript
// 1.在components目录下封装一个组件
import { getToken } from '@/utils'
import { Navigate } from 'react-router-dom'

export function AuthRouter ({ children }) {
    const token = getToken()
    if(token){
        return <>{children}</>
    }else{
        return <Navigate to={'/login'} replace />
    }
}


// 2.在router目录的index.js中找到需要鉴权的路由，进行修改
import Layout from '@/page/Layout'
import { createBrowserRouter } from 'react-router-dom'
import { AuthRouter } from '@/components/AuthRouter'
const router = createBrowserRouter([
    {
        path:'/',
        element:<AuthRouter><Layout /></AuthRouter>
    }
])

export default router
```

### 样式初始化

```JavaScript
// 
npm install normalize.css

//2.在根目录的index.js中导入
import 'normalize.css'
```

### 路由懒加载

1\.把路由修改为由react提供的lazy函数进行动态导入

```JavaScript
// ./router/index.js
// import Home from '@/pages/Home'
// 1. lazy函数对组件进行导入
const Home = lazy(() => import('@/pages/Home'))
```

2\.使用react内置的suspense组件包裹路由中element属性对应的组件

```javascript
// 包裹后
const router = createBrowserRouter([
  {
    path: "/",
    element: <AuthRoute> <Layout /></AuthRoute>,
    children: [
      {
        index: true,
        element: <Suspense fallback={'加载中'}><Home /></Suspense>
      },
      {
        path: 'article',
        element: <Suspense fallback={'加载中'}><Article /></Suspense>
      },
      {
        path: 'publish',
        element: <Suspense fallback={'加载中'}><Publish /></Suspense>
      }
    ]
  },
  {
    path: "/login",
    element: <Login />
  }
])

// 包裹前
const router = createBrowserRouter([
  {
    path: "/",
    element: <AuthRoute> <Layout /></AuthRoute>,
    children: [
      {
        index: true,
        element: <Home />
      },
      {
        path: 'article',
        element: <Article />
      },
      {
        path: 'publish',
        element: <Publish />
      }
    ]
  },
  {
    path: "/login",
    element: <Login />
  }
])
```

### Cdn

```JavaScript
// craco.config.js
// 扩展webpack的配置

const path = require('path')
// 引入辅助函数
const { whenProd, getPlugin, pluginByName } = require('@craco/craco')

module.exports = {
  // webpack 配置
  webpack: {
    // 配置别名
    alias: {
      // 约定：使用 @ 表示 src 文件所在路径
      '@': path.resolve(__dirname, 'src')
    },
    // 配置CDN
    configure: (webpackConfig) => {
      let cdn = {
        js: []
      }
      whenProd(() => {
        // key: 不参与打包的包(由dependencies依赖项中的key决定)
        // value: cdn文件中 挂载于全局的变量名称 为了替换之前在开发环境下
        webpackConfig.externals = {
          react: 'React',
          'react-dom': 'ReactDOM'
        }
        // 配置现成的cdn资源地址
        // 实际开发的时候 用公司自己花钱买的cdn服务器
        cdn = {
          js: [
            'https://cdnjs.cloudflare.com/ajax/libs/react/18.1.0/umd/react.production.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.1.0/umd/react-dom.production.min.js',
          ]
        }
      })
      // 通过 htmlWebpackPlugin插件 在public/index.html注入cdn资源url
      const { isFound, match } = getPlugin(
        webpackConfig,
        pluginByName('HtmlWebpackPlugin')
      )

      if (isFound) {
        // 找到了HtmlWebpackPlugin的插件
        match.userOptions.cdn = cdn
      }
      return webpackConfig
    }
  },
}
```

```JavaScript
// ../public/index.html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#000000" />
  <meta name="description" content="Web site created using create-react-app" />
  <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
  <!--
      manifest.json provides metadata used when your web app is installed on a
      user's mobile device or desktop. See https://developers.google.com/web/fundamentals/web-app-manifest/
    -->
  <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
  <!--
      Notice the use of %PUBLIC_URL% in the tags above.
      It will be replaced with the URL of the `public` folder during the build.
      Only files inside the `public` folder can be referenced from the HTML.

      Unlike "/favicon.ico" or "favicon.ico", "%PUBLIC_URL%/favicon.ico" will
      work correctly both with client-side routing and a non-root public URL.
      Learn how to configure a non-root public URL by running `npm run build`.
    -->
  <title>React App</title>
</head>

<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
  <!-- 动态插入cdn资源url -->
  <% htmlWebpackPlugin.options.cdn.js.forEach(cdnURL=> { %>
    <script src="<%= cdnURL %>"></script>
    <% }) %>
</body>

</html>
```

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

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTQwZTkxZWZkODRjYzE0OGVmZWEzNmQ0NzFkZDYxOTJfYjdiNDk4NWI2ZTEyY2U0MzdhNzY2MWQwN2IxZjI4YzJfSUQ6NzUwMTAzMDk2NjU4OTIxMDYyNl8xNzgyMzE5MDc5OjE3ODI0MDU0NzlfVjM)

解决（赋默认值，就不会为undefined）：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NGNkZDE2MTE1N2MwMDM1M2NiNzRlOGNlN2NiZTA1ZmFfMGZiNTJjYTEwY2ZhZTUzMjRlMzU4OTVlZmRiM2IyOTJfSUQ6NzUwMTAzMTAzMjY0MTA5MzYzNF8xNzgyMzE5MDc5OjE3ODI0MDU0NzlfVjM)





# 项目开发技术栈选型

- **框架**：Next\.js 16 \(App Router\)

- **语言**：TypeScript

- **UI**：React 19

- **样式**：Tailwind CSS \+ 自己的 design tokens

- **组件基础**：Radix UI / shadcn/ui 这一类方案

- **数据层**：首屏用 Next 的服务端能力，交互数据用 TanStack Query

- **轻状态管理**：Zustand

- **表单校验**：react\-hook\-form \+ zod \+server action

- **媒体能力**：图片 CDN \+ next/image；如果有长视频和清晰度切换，再上 hls\.js

- **测试**：Playwright 做关键链路，Vitest 做单测

- **监控**：Sentry \+ 埋点分析体系











函数式组件vsclass组件：推荐使用函数式组件

tsx的情况，function外面一般用来定义导入以及类型声明

父传子：props

子传父：父组件声明一个回调函数，子组件往父组件的回调函数中传参

对于usestate这个hook，更新值的时候一定要在set方法里面去更新，否则不会响应式变化。



以下的方式配合usecallback很好用

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDNlZTMwMTFmYzVkMTVhZTAxZGE4MWJmZTExMGE0NDJfNGI1ZjRkNmU1NmZlNGU4M2E4YzBmZDQzZmFlM2UzZWNfSUQ6NzYyNDc3MjEyMjk3OTYxNzk4NV8xNzgyMzE5MDc5OjE3ODI0MDU0NzlfVjM)



ref作用：获取dom，存储不在视图上更新的一些值

注意事项：

1. 组件在重新渲染的时候，useRef的值不会被重新初始化。

2. 改变 ref\.current 属性时，React 不会重新渲染组件。React 不知道它何时会发生改变，因为 ref 是一个普通的 JavaScript 对象。

3. useRef的值不能作为useEffect等其他hooks的依赖项，因为它并不是一个响应式状态。

4. useRef不能直接获取子组件的实例，需要使用forwardRef。



表单提交：action，以及useactionstate，useformstate





suspense\+lazy实现组件的懒加载以及代码拆分

配合use方法替代常规的写法

常规写法：关注loading状态，以及使用useeffect在组件挂载的时候发起异步请求

render\-as\-you\-fetch

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NjNlMTI4MDg4ZTQzMWEyZWM2MGMwYTQ4M2JiZTg5Y2RfNjk4MGE0NDI3ZDg4OWU5YjAxMjU4NGY5ZjMzZDJmYWVfSUQ6NzYyNDc4MjU1NjQ2NjMwMjE3Nl8xNzgyMzE5MDc5OjE3ODI0MDU0NzlfVjM)





性能优化usememo，usecallback，react\.memo，缓存属性，或者缓存方法，就不需要每次调用的时候新建，性能更好



通过compiler插件，可以在编译的时候做性能优化

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZTY2NGVhZjYwY2ZmMTViNmNkZjE5ODAzYzM4OTY4NzlfYTQ5ZjM4MzZhMzIzZTcxMmI3YmVkYmI1OWM4YmJmZTlfSUQ6NzYyNDc4NDcxODQ4MzA5ODU4Ml8xNzgyMzE5MDc5OjE3ODI0MDU0NzlfVjM)







usestate的使用重点：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MzJjYjhkYWQ4YjYyZGQyYTU5ZmUxY2VlODliM2E2MmNfYzVlNTRkYzM5ZTdjODllNjlmYWFiNWQ3N2M1ODEyZmJfSUQ6NzYyNDc4NjE3Mjc4MjM4MjI5OV8xNzgyMzE5MDc5OjE3ODI0MDU0NzlfVjM)



userducer管理复杂数据类型，比如说管理的数据类型是一个对象，就可以用usereducer





深层状态传递：context





zod对运行时的数据类型进行检查







# react项目开发

Npm create 项目名称 \-\-template=react\-ts

react\-router\&\&react\-router\-dom，版本号保持一致

tanstack/react\-query

zustand

React\-hook\-form

zod





# next项目开发

路由：app\-router

组件：默认是server component，还有client component（需要在文件最上面添加useclient）

嵌套逻辑：一般都是server component里面去定义client component，如果client component里面有server component，它会自动变成client component

Server component：里面定义一些常量，最终返回的是html，所以只能写好一些静态的东西

Client component：可以使用一些hooks，比如说usestate

Nextjs route handler





构建工具：turbopack





通过ref和useeffect实现只要聊天消息有变化，都会回到底部



修复高危漏洞：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Y2FjZjZhMjg0YWYyOTlhMGM0MjRiYTFlM2U1NDRmY2JfNzhjMjIyMzFmM2E3ZGNkZWE5YjRhNzA0NWQyYzljYzNfSUQ6NzYyNTI1OTE2NzIxNjkxMzU5OV8xNzgyMzE5MDc5OjE3ODI0MDU0NzlfVjM)





空心圆表示静态内容，f表示动态，静态内容会缓存，如果里面有像发请求的，就会缓存第一次请求的结果，后续不再重新请求。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NGE4MTMyNGIxNWEwY2IyZDNjZGM4ZjM0YTU3ZWIzNzhfNTI5ZGE1N2VlODQzMDZmZDM1OGQ3NGZjYzc1MTFlMzRfSUQ6NzYyNTMxNjUwNDY2OTYwNTA2MV8xNzgyMzE5MDc5OjE3ODI0MDU0NzlfVjM)





什么是ssg：

纯静态页面，比如说技术文档这些没有交互的东西，就可以使用ssg





mdx：markdown里面可以嵌套react组件





页面需要拆分成多个组件时的目录结构：

page\.tsx 只是这个路由的入口组件，不需要把所有 tsx 都堆进去。更常见的做法是让 page\.tsx 只负责“组装页面”，把大块内容拆到普通组件里，也就是\_component目录下面的文件：

```Java
src/
└── app/
    └── xiaoman/
        ├── page.tsx
        ├── _components/
        │   ├── Hero.tsx
        │   ├── ArticleList.tsx
        │   └── Footer.tsx
        └── _lib/
            └── data.ts

```

几个建议：

- 只在路由入口放 page\.tsx，其余页面块拆成普通组件。

- 某个页面专用的组件，就放在这个路由目录下，比如 app/xiaoman/\_components。

- 多个页面都会复用的组件，再提到 src/components。

- 如果某个拆出去的组件用了 useState、useEffect、点击事件这些客户端能力，就只在那个组件文件顶部加 'use client'，不要一上来把整个 page\.tsx 都变成客户端组件。

- 官方也明确说明了：app 里可以安全地 colocate 项目文件；而 \_folder 这种私有文件夹会被排除出路由系统，特别适合放 \_components、\_lib 这类内部实现文件。

正常的项目结构：

```Java
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── xiaoman/
│   │   ├── page.tsx
│   │   ├── loading.tsx
│   │   ├── error.tsx
│   │   ├── _components/
│   │   │   ├── Hero.tsx
│   │   │   ├── ArticleList.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── _lib/
│   │   │   ├── data.ts
│   │   │   └── format.ts
│   │   └── _types/
│   │       └── index.ts
│   └── daman/
│       ├── page.tsx
│       ├── _components/
│       │   └── Hero.tsx
│       └── _lib/
│           └── data.ts
├── components/
│   └── ui/
│       ├── Button.tsx
│       └── Card.tsx
├── lib/
│   ├── request.ts
│   └── utils.ts
└── types/
    └── global.ts
```

但是组件也可以直接放在页面目录下面，只要他不是特殊文件名，比如page\.tsx、layout\.tsx、template\.tsx、loading\.tsx、error\.tsx、not\-found\.tsx、route\.ts就完全可以。

```Java
src/
└── app/
    └── xiaoman/
        ├── page.tsx
        ├── Hero.tsx
        ├── ArticleList.tsx
        └── _lib/
            └── data.ts
```

更常用的项目结构：

```Java
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   ├── (marketing)/
│   │   ├── page.tsx
│   │   ├── about/
│   │   │   └── page.tsx
│   │   └── contact/
│   │       └── page.tsx
│   ├── (main)/
│   │   ├── xiaoman/
│   │   │   ├── page.tsx
│   │   │   ├── loading.tsx
│   │   │   ├── error.tsx
│   │   │   └── not-found.tsx
│   │   └── daman/
│   │       └── page.tsx
│   └── api/
│       └── articles/
│           └── route.ts
├── features/
│   ├── xiaoman/
│   │   ├── components/
│   │   │   ├── Hero.tsx
│   │   │   ├── ArticleList.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── services/
│   │   │   └── getXiaomanData.ts
│   │   ├── hooks/
│   │   │   └── useXiaomanFilter.ts
│   │   ├── types.ts
│   │   └── utils.ts
│   └── daman/
│       ├── components/
│       ├── services/
│       └── types.ts
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Modal.tsx
│   └── shared/
│       ├── Header.tsx
│       └── Footer.tsx
├── lib/
│   ├── request.ts
│   ├── auth.ts
│   ├── db.ts
│   └── utils.ts
├── hooks/
│   └── useDebounce.ts
├── store/
│   └── userStore.ts
├── constants/
│   └── index.ts
└── types/
    └── global.d.ts
```

- app：只放路由相关文件，像 page\.tsx、layout\.tsx、loading\.tsx、error\.tsx、route\.ts

- features：按业务模块拆分，比如“小满模块”“大满模块”

- components/ui：通用 UI 组件，任何页面都能复用

- components/shared：站点级公共组件，比如头部、底部

- lib：跨业务的工具、请求、鉴权、数据库

- hooks/store/types/constants：全局能力





# 样式方案

## 1\.css module

在 React 里，CSS Module 就是：

1. 把样式文件写成 xxx\.module\.css

2. 在组件里 import styles from '\./xxx\.module\.css'

3. 用 className=\{styles\.xxx\} 绑定类名

4. 构建后自动生成唯一类名，实现样式隔离



## 2\.css\-in\-js

优势：

- 样式和组件靠得很近，维护方便

- 动态样式很好写

- 通常也有样式隔离，不容易冲突

- 适合做主题切换、组件库、复杂交互样式

```JavaScript
// 代码示例
import styled from 'styled-components';

const Button = styled.button`
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  background: ${(props) => (props.danger ? '#dc2626' : '#2563eb')};
`;

function App() {
  return (
    <>
      <Button>保存</Button>
      <Button danger>删除</Button>
    </>
  );
}

export default App;
```

## 3\.tailwindcss

