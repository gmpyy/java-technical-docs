---
title: React 全系列技术文档
description: 按 React 核心模型、组件、状态、Hooks、路由、状态管理、渲染性能和工程实践整理的完整技术文档。
outline: [2, 3]
---

# React 全系列技术文档

这套文档把 React 系列资料整理成面向开发实践的技术文档。它不采用问答清单的形式，而是把每个主题拆到“概念、原理、写法、边界、代码示例、实践建议”中，方便在项目开发、复盘和知识补齐时查阅。

React 的核心可以概括为：用组件描述界面，用状态驱动变化，用单向数据流约束复杂度，用虚拟 DOM 和 Fiber 调和更新，用生态工具补齐路由、状态管理、样式、动画、服务端渲染和错误治理。

```tsx
import { useState } from 'react'

export function CounterPanel() {
  const [count, setCount] = useState(0)

  return (
    <section>
      <h2>当前计数：{count}</h2>
      <button onClick={() => setCount((value) => value + 1)}>
        增加
      </button>
    </section>
  )
}
```

上面的组件体现了 React 的基本工作方式：组件返回 UI 描述，事件触发状态更新，React 根据新旧描述计算差异，再把必要变化提交到界面。

## 阅读路径

如果刚开始系统整理 React，可以按下面顺序阅读：

1. 先看 [React 基础模型](/react-series/foundation)，理解 React、Real DOM、Virtual DOM 和 JSX 到界面的过程。
2. 再看 [组件系统](/react-series/components)，掌握组件构建、事件、通信、key、refs、表单和复用模式。
3. 接着看 [状态与生命周期](/react-series/state-lifecycle)，把 props、state、`setState`、生命周期和 render 触发串起来。
4. 然后看 [Hooks、样式与动画](/react-series/hooks-style-animation)，理解函数组件时代的逻辑组织方式和 UI 表现层。
5. 再看 [路由与状态管理](/react-series/routing-state)，补齐 React Router、Redux、middleware、immutable 和项目结构。
6. 继续看 [渲染与性能](/react-series/rendering-performance)，掌握 diff、Fiber、render 机制和性能优化。
7. 最后看 [工程实践](/react-series/engineering)，覆盖错误捕获、SSR 和常见项目问题。
8. 检查完整性时看 [来源覆盖表](/react-series/coverage)，逐项确认 33 个主题都已覆盖。

## 章节地图

| 章节 | 内容范围 |
| --- | --- |
| React 基础模型 | React 概念与特性、Real DOM 与 Virtual DOM、JSX 转换为真实 DOM |
| 组件系统 | 事件机制、事件绑定、组件构建、组件通信、key、refs、组件类型、表单、高阶组件 |
| 状态与生命周期 | 生命周期阶段、state 与 props、`super()` 与 `super(props)`、`setState`、render 触发 |
| Hooks、样式与动画 | React Hooks、CSS 引入方式、组件过渡动画 |
| 路由与状态管理 | Redux、middleware、Redux 项目结构、React Router、Router 模式、immutable |
| 渲染与性能 | render 原理、避免无效渲染、diff、Fiber、性能优化 |
| 工程实践 | 错误捕获、服务端渲染、常见问题与解决方式 |
| 来源覆盖表 | 33 个来源主题到目标章节的映射 |

## 文档整理原则

这套文档遵循四个约束：

| 原则 | 说明 |
| --- | --- |
| 完整覆盖 | 33 个主题都在覆盖表中出现，并映射到正文位置 |
| 技术文档化 | 使用开发者视角表达，不保留来源站点的考察语境 |
| 保留核心代码 | 关键 API、更新流程、组件写法和工程结构都保留示例 |
| 不依赖远程资源 | 正文不引用远程图片、脚本或第三方站点资源 |

## 快速心智模型

### 组件是 UI 的函数

函数组件接收 props，返回 React Element。类组件也是描述式模型，只是状态、生命周期和方法挂在实例上。

```tsx
type UserCardProps = {
  name: string
  role: string
}

export function UserCard({ name, role }: UserCardProps) {
  return (
    <article>
      <h3>{name}</h3>
      <p>{role}</p>
    </article>
  )
}
```

### 状态改变驱动界面改变

React 不鼓励直接操作 DOM 来同步 UI，而是通过状态入口发起变化。

```tsx
function ToggleLabel() {
  const [enabled, setEnabled] = useState(false)

  return (
    <label>
      <input
        type="checkbox"
        checked={enabled}
        onChange={(event) => setEnabled(event.target.checked)}
      />
      {enabled ? '已启用' : '未启用'}
    </label>
  )
}
```

### 单向数据流让变化可追踪

父组件向下传数据，子组件通过回调向上传递动作。复杂场景再引入 Context、路由状态、Redux 或其他状态层。

```tsx
function SearchPage() {
  const [keyword, setKeyword] = useState('')

  return (
    <>
      <SearchInput value={keyword} onChange={setKeyword} />
      <ResultList keyword={keyword} />
    </>
  )
}
```

## 验收方式

验收时建议按下面顺序检查：

1. 打开 [来源覆盖表](/react-series/coverage)，逐项核对 33 个技术主题。
2. 检查每个主题是否能在正文中找到概念、原理、用法或实践说明。
3. 搜索站点中是否残留来源站点语境词。
4. 运行测试和 VitePress 构建，确保文档可发布。

