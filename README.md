# Travel Plan Service 旅行规划服务

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 项目概述

Travel Plan Service 是一个基于 AI 的智能旅行规划服务，使用 SSE (Server-Sent Events) 实现实时流式响应，提供个性化旅行攻略生成服务。

**核心特点**：
- 🚀 流式响应：使用 SSE 技术实现打字机效果
- 📝 Markdown 渲染：支持富文本格式的旅行计划展示

## 技术栈

- 前端：Vue 3
- 后端：FastAPI
- 通信：Server-Sent Events (SSE)
- 文档渲染：Marked.js

## 快速开始

### 安装依赖

```bash
# 后端依赖
uv sync

# 前端依赖
npm install
```

### 环境配置

创建 `.env` 文件：

```env
LLM_MODEL=your_model_name
LLM_BASE_URL=your_base_url
LLM_API_KEY=your_api_key
```

### 启动服务

```bash
# 启动后端
uv run main.py

# 启动前端（新终端）
npm run dev
```

## API 文档

### 旅行规划 SSE 接口

**GET /travel-plan/stream**

支持流式响应的旅行规划生成接口。

请求参数：
```
query: string  // 旅行需求描述
```

SSE 事件类型：
- `start`: 开始生成
- `message`: 内容片段
- `complete`: 生成完成
- `error`: 发生错误

响应示例：
```javascript
// message 事件
event: message
data: 这是一段旅行计划内容...

// complete 事件
event: complete
data: 规划完成

// error 事件
event: error
data: 错误信息
```

## 前端集成

### Vue 3 组件示例

```vue
<script setup>
import { ref, onUnmounted } from 'vue'

const query = ref('')
const content = ref('')
const loading = ref(false)
let eventSource = null

const initSSE = () => {
  const url = `/travel-plan/stream?query=${encodeURIComponent(query.value)}`
  eventSource = new EventSource(url)

  eventSource.addEventListener('message', (event) => {
    content.value += event.data
  })

  eventSource.addEventListener('complete', () => {
    loading.value = false
    closeConnection()
  })

  eventSource.addEventListener('error', () => {
    // 错误处理逻辑
  })
}

// 组件销毁时清理
onUnmounted(() => {
  if (eventSource) {
    eventSource.close()
  }
})
</script>
```

## License

MIT