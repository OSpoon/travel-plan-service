# Travel Plan Service 旅行规划服务

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 项目概述

Travel Plan Service 是一个基于 AI 的智能旅行规划服务，使用 FastAPI StreamingResponse 实现实时流式响应，提供个性化旅行攻略生成服务。

**核心特点**：
- 🚀 流式响应：使用 StreamingResponse 技术实现打字机效果
- 📝 Markdown 渲染：支持富文本格式的旅行计划展示

## 技术栈

- 前端：Vue 3
- 后端：FastAPI
- 通信：StreamingResponse
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

### 旅行规划流式接口

**POST /travel-plan/stream**

使用 StreamingResponse 实现的流式响应接口。

请求参数：
```json
{
  "query": "string"  // 旅行需求描述
}
```

响应格式：
```json
// 正常内容块
{"content": "这是一段旅行计划内容..."}

// 完成标记
{"status": "complete"}

// 错误信息
{"error": "错误描述"}
```

## 前端集成

### Vue 3 示例

```vue
<script setup>
const query = ref('')
const content = ref('')
const loading = ref(false)
let abortController = null

const submitQuery = async () => {
  // 取消已有请求
  if (abortController) {
    abortController.abort()
  }

  abortController = new AbortController()
  loading.value = true

  try {
    const response = await fetch('/travel-plan/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query.value }),
      signal: abortController.signal
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { value, done } = await reader.read()
      // 处理流式数据...
    }
  } catch (error) {
    // 错误处理...
  }
}

onUnmounted(() => {
  if (abortController) {
    abortController.abort()
  }
})
</script>
```

### 数据流处理

1. 请求控制
   - 使用 AbortController 管理请求生命周期
   - 组件卸载时自动取消请求
   - 新请求发起时取消旧请求

2. 流式数据处理
   - 使用 ReadableStream 接收数据流
   - TextDecoder 解码二进制数据
   - 按行解析 JSON 数据

3. 错误处理
   - 区分请求取消和其他错误
   - 友好的错误提示
   - 自动重置加载状态

## License

MIT