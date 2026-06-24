---
title: "React Notes: Redux"
description: "React.md source note section: Redux."
outline: [2, 3]
---

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
