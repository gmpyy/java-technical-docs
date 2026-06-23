---
title: React 全系列来源覆盖表
description: React 全系列 33 个技术主题到目标文档章节的覆盖关系。
outline: [2, 3]
---

# React 全系列来源覆盖表

这张表用于逐项验收完整性。左侧是整理后的技术主题名，右侧是正文落点。主题名保留技术含义，但改成文档化表达。

| 序号 | 技术主题 | 目标章节 | 覆盖重点 |
| --- | --- | --- | --- |
| 1 | React 概念与特性 | [React 基础模型](/react-series/foundation) | 声明式 UI、组件化、单向数据流、JSX、虚拟 DOM、生态边界 |
| 2 | Real DOM 与 Virtual DOM | [React 基础模型](/react-series/foundation) | DOM 操作成本、虚拟 DOM 描述对象、优缺点和适用边界 |
| 3 | React 生命周期阶段 | [状态与生命周期](/react-series/state-lifecycle) | 挂载、更新、卸载、错误阶段和新旧生命周期迁移 |
| 4 | state 与 props | [状态与生命周期](/react-series/state-lifecycle) | 数据来源、可变性、更新入口、派生状态风险 |
| 5 | super() 与 super(props) | [状态与生命周期](/react-series/state-lifecycle) | ES class 继承、类组件 constructor、`this.props` 初始化时机 |
| 6 | setState 执行机制 | [状态与生命周期](/react-series/state-lifecycle) | 更新队列、批处理、函数式更新、提交后回调 |
| 7 | React 事件机制 | [组件系统](/react-series/components) | SyntheticEvent、事件代理、捕获冒泡、React 17 根容器委托 |
| 8 | React 事件绑定方式 | [组件系统](/react-series/components) | constructor bind、class field、JSX 箭头函数、参数传递 |
| 9 | React 组件构建方式 | [组件系统](/react-series/components) | 函数组件、类组件、`React.createClass`、组件实例与元素 |
| 10 | React 组件通信 | [组件系统](/react-series/components) | 父子、跨级、非嵌套、发布订阅、Context、状态提升 |
| 11 | key 的作用 | [组件系统](/react-series/components) | 同层节点身份、列表复用、状态错位和稳定 key |
| 12 | refs 的理解与应用 | [组件系统](/react-series/components) | DOM 访问、命令式方法、`forwardRef`、`useImperativeHandle` |
| 13 | 类组件与函数组件 | [组件系统](/react-series/components) | 状态模型、生命周期、this、逻辑复用和现代选择 |
| 14 | 受控组件与非受控组件 | [组件系统](/react-series/components) | 表单值来源、校验联动、文件输入和 ref 读取 |
| 15 | 高阶组件 | [组件系统](/react-series/components) | 逻辑复用、横切能力、props 透传、ref 处理 |
| 16 | React Hooks | [Hooks、样式与动画](/react-series/hooks-style-animation) | Hook 顺序、状态单元、常用 Hook、自定义 Hook、闭包依赖 |
| 17 | React 中 CSS 引入方式 | [Hooks、样式与动画](/react-series/hooks-style-animation) | 普通 CSS、CSS Modules、预处理器、CSS-in-JS、原子化样式 |
| 18 | React 组件过渡动画 | [Hooks、样式与动画](/react-series/hooks-style-animation) | CSS transition、CSSTransition、动画状态、卸载时机 |
| 19 | Redux 理解与工作原理 | [路由与状态管理](/react-series/routing-state) | store、action、reducer、dispatch、订阅更新 |
| 20 | Redux middleware | [路由与状态管理](/react-series/routing-state) | dispatch 增强、三层柯里化、异步、日志、错误处理 |
| 21 | React 项目中的 Redux 使用与结构划分 | [路由与状态管理](/react-series/routing-state) | store 配置、slice、模块边界、容器组件和选择器 |
| 22 | React Router 理解与常用组件 | [路由与状态管理](/react-series/routing-state) | Router、Routes、Route、Link、Navigate、Outlet |
| 23 | React Router 模式与实现原理 | [路由与状态管理](/react-series/routing-state) | BrowserRouter、HashRouter、MemoryRouter、StaticRouter |
| 24 | immutable 在 React 中的应用 | [路由与状态管理](/react-series/routing-state) | 不可变更新、浅比较、结构共享、常见写法 |
| 25 | React render 原理与触发时机 | [渲染与性能](/react-series/rendering-performance) | state、props、Context、forceUpdate、render 阶段与 commit 阶段 |
| 26 | 提高组件渲染效率 | [渲染与性能](/react-series/rendering-performance) | 状态位置、组件拆分、memo、缓存、虚拟列表 |
| 27 | React diff 原理 | [渲染与性能](/react-series/rendering-performance) | 类型比较、同层比较、key、子节点移动和替换 |
| 28 | Fiber 架构 | [渲染与性能](/react-series/rendering-performance) | 可中断渲染、工作单元、优先级、双缓存树 |
| 29 | JSX 转换为真实 DOM | [React 基础模型](/react-series/foundation) | JSX 编译、React Element、Fiber、提交 DOM |
| 30 | React 性能优化手段 | [渲染与性能](/react-series/rendering-performance) | 渲染范围、计算缓存、代码分割、列表优化、并发能力 |
| 31 | React 错误捕获 | [工程实践](/react-series/engineering) | Error Boundary、`getDerivedStateFromError`、`componentDidCatch`、运行时兜底 |
| 32 | React 服务端渲染 | [工程实践](/react-series/engineering) | SSR 流程、hydration、数据预取、同构差异 |
| 33 | React 常见问题与解决方式 | [工程实践](/react-series/engineering) | key、闭包、effect、状态派生、性能、样式、路由刷新 |

## 覆盖检查方法

验收时可以按下面流程做逐项检查：

```powershell
rg -n "React 概念与特性|Real DOM 与 Virtual DOM|React 生命周期阶段" docs/react-series
rg -n "Redux middleware|Fiber 架构|React 服务端渲染" docs/react-series
python -m unittest tests/test_vitepress_docs.py
```

如果某个主题只在本覆盖表中出现，而没有在正文中展开，应继续补充对应章节。本次整理的正文按主题合并，不要求来源目录和目标目录一一同名，但必须保证每个主题都能在正文中找到可读的技术说明。
