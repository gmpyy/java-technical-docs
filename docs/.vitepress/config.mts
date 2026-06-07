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
      { text: 'React', link: '/react/' },
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
