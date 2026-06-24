---
title: "React Notes: Stack Selection"
description: "React.md source note section: Stack Selection."
outline: [2, 3]
---

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

![Image](/images/react-notes/image-04.png)



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

![Image](/images/react-notes/image-05.png)





性能优化usememo，usecallback，react\.memo，缓存属性，或者缓存方法，就不需要每次调用的时候新建，性能更好



通过compiler插件，可以在编译的时候做性能优化

![Image](/images/react-notes/image-06.png)







usestate的使用重点：

![Image](/images/react-notes/image-07.png)



userducer管理复杂数据类型，比如说管理的数据类型是一个对象，就可以用usereducer





深层状态传递：context





zod对运行时的数据类型进行检查
