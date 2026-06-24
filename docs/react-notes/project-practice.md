---
title: "React Notes: Project Practice"
description: "React.md source note section: Project Practice."
outline: [2, 3]
---

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
