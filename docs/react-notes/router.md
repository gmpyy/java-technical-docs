---
title: "React Notes: React Router"
description: "React.md source note section: React Router."
outline: [2, 3]
---

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
