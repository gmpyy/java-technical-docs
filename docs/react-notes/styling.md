---
title: "React Notes: Styling"
description: "React.md source note section: Styling."
outline: [2, 3]
---

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
