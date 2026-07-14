import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '技术文档',
  description: '从 Java 后端到 React 前端的系统化学习文档',
  base: '/java-technical-docs/',
  lang: 'zh-CN',
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    logo: '/images/logo.svg',
    search: {
      provider: 'local'
    },
    nav: [
      { text: '首页', link: '/' },
      { text: 'Vue', link: '/vue/' },
      { text: 'Vue 知识体系', link: '/vue-knowledge/' },
      { text: 'React', link: '/react/' },
      { text: 'React 全系列', link: '/react-series/' },
      { text: 'React 原文笔记', link: '/react-notes/' },
      { text: 'Java', link: '/java/basic' },
      { text: 'Spring Boot', link: '/springboot/project' },
      { text: 'Redis', link: '/redis/basics' }
    ],
    sidebar: [
      {
        text: '总览',
        items: [
          { text: '文档首页', link: '/' }
        ]
      },
      {
        text: 'Vue 技术文档',
        collapsed: false,
        items: [
          { text: 'Vue 总览', link: '/vue/' },
          { text: '项目主线', link: '/vue/project' },
          { text: '核心基础', link: '/vue/basics' },
          { text: 'Composition API', link: '/vue/composition' },
          { text: '组件与路由', link: '/vue/components-router' },
          { text: '状态与请求', link: '/vue/state-request' },
          { text: 'UI、项目与旧项目维护', link: '/vue/ui-projects-legacy' }
        ]
      },
      {
        text: 'Vue 知识体系',
        collapsed: false,
        items: [
          { text: 'Vue 知识体系总览', link: '/vue-knowledge/' },
          { text: '一、Vue 基础', link: '/vue-knowledge/basics' },
          { text: '二、生命周期', link: '/vue-knowledge/lifecycle' },
          { text: '三、组件通信', link: '/vue-knowledge/component-communication' },
          { text: '四、路由', link: '/vue-knowledge/router' },
          { text: '五、Vuex', link: '/vue-knowledge/vuex' },
          { text: '六、Vue 3.0', link: '/vue-knowledge/vue3' },
          { text: '七、虚拟DOM', link: '/vue-knowledge/virtual-dom' }
        ]
      },
      {
        text: 'React 技术文档',
        collapsed: false,
        items: [
          { text: 'React 总览', link: '/react/' },
          { text: '组件基础', link: '/react/component-basics' },
          { text: '状态与生命周期', link: '/react/state-lifecycle' },
          { text: 'Hooks', link: '/react/hooks' },
          { text: '渲染机制', link: '/react/rendering' },
          { text: '通信、路由与状态管理', link: '/react/router-state' },
          { text: '工程实践', link: '/react/ecosystem-practice' }
        ]
      },
      {
        text: 'React 全系列技术文档',
        collapsed: false,
        items: [
          { text: 'React 全系列总览', link: '/react-series/' },
          { text: 'React 基础模型', link: '/react-series/foundation' },
          { text: '组件系统', link: '/react-series/components' },
          { text: '状态与生命周期', link: '/react-series/state-lifecycle' },
          { text: 'Hooks、样式与动画', link: '/react-series/hooks-style-animation' },
          { text: '路由与状态管理', link: '/react-series/routing-state' },
          { text: '渲染与性能', link: '/react-series/rendering-performance' },
          { text: '工程实践', link: '/react-series/engineering' },
          { text: '来源覆盖表', link: '/react-series/coverage' }
        ]
      },
      {
        text: 'React 原文笔记',
        collapsed: false,
        items: [
          { text: 'React 原文笔记总览', link: '/react-notes/' },
          { text: 'React 基础', link: '/react-notes/basics' },
          { text: 'Redux', link: '/react-notes/redux' },
          { text: 'React 路由', link: '/react-notes/router' },
          { text: '实际项目开发', link: '/react-notes/project-practice' },
          { text: 'React 高级', link: '/react-notes/advanced' },
          { text: 'Zustand', link: '/react-notes/zustand' },
          { text: 'React + TS', link: '/react-notes/react-ts' },
          { text: '技术栈选型', link: '/react-notes/stack-selection' },
          { text: 'React 项目开发', link: '/react-notes/react-project' },
          { text: 'Next 项目开发', link: '/react-notes/next-project' },
          { text: '样式方案', link: '/react-notes/styling' },
          { text: '原文归档', link: '/react-notes/source' }
        ]
      },
      {
        text: 'Java 基础',
        collapsed: false,
        items: [
          { text: '基础语法与类型', link: '/java/basic' },
          { text: '方法、IO 与 JavaBean', link: '/java/syntax' },
          { text: '字符串与集合', link: '/java/string-collections' },
          { text: '面向对象进阶', link: '/java/oop' },
          { text: '生态与数据库基础', link: '/java/ecosystem-database' }
        ]
      },
      {
        text: 'Spring Boot',
        collapsed: false,
        items: [
          { text: '项目结构与分层', link: '/springboot/project' },
          { text: '请求参数、DI 与 MyBatis', link: '/springboot/request-di-mybatis' },
          { text: 'Filter、Interceptor 与 CORS', link: '/springboot/web-chain' },
          { text: 'JWT 与验证码认证', link: '/springboot/auth' },
          { text: '事务与定时任务', link: '/springboot/reliability' }
        ]
      },
      {
        text: '消息与缓存',
        collapsed: false,
        items: [
          { text: 'RabbitMQ 消息队列', link: '/middleware/rabbitmq' },
          { text: 'Redis 基础与登录链路', link: '/redis/basics' },
          { text: '缓存、锁与秒杀', link: '/redis/cache-lock' },
          { text: 'Redis 高级结构', link: '/redis/advanced' }
        ]
      }
    ],
    outline: {
      level: [2, 3],
      label: '本页目录'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    footer: {
      message: '基于技术资料重构整理',
      copyright: '技术文档'
    }
  }
})
