# Travel Plan Service 旅行规划服务

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 目录

- 项目概述
- 主要功能
- 快速开始
- API 文档
- 前端集成
- 开发指南
- 常见问题

## 项目概述

Travel Plan Service 是一个基于 AI 的智能旅行规划服务，可以根据用户需求自动生成个性化旅行攻略。系统利用先进的语言模型，结合地图服务和旅游数据，提供全面且实用的旅行建议。

**核心亮点**：
- 🤖 智能规划：基于大型语言模型的个性化旅行方案
- 🔄 实时响应：支持流式输出，提供即时反馈
- 🔌 易于集成：RESTful API 设计，支持各类前端应用
- 🗺️ 地图集成：内置地图服务支持，提供导航建议

## 主要功能

- **个性化旅行规划**：生成包含景点、餐饮、交通、住宿的完整方案
- **行程优化**：根据距离、开放时间、游览时长自动优化路线
- **预算估算**：提供各项费用的参考价格，帮助控制旅行成本
- **流式响应**：支持打字机式实时内容展示，提升用户体验
- **灵活配置**：通过环境变量轻松调整模型参数和 API 设置

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/travel-plan-service.git
cd travel-plan-service

# 安装依赖
pip install -e .

# 配置环境
cp .env.example .env
# 编辑 .env 文件填入必要配置
```

### 配置

在 .env 文件中设置以下参数：

```
LLM_MODEL=your_model_name
LLM_BASE_URL=your_base_url
LLM_API_KEY=your_api_key

AMAP_KEY=your_amap_key  # 高德地图API密钥(可选)
```

### 启动服务

```bash
python main.py
```

服务默认在 `http://localhost:8000` 启动

### 示例请求

```bash
curl -X POST "http://localhost:8000/travel-plan" \
     -H "Content-Type: application/json" \
     -d '{"query": "帮我规划一个为期3天的北京旅行计划"}'
```

## API 文档

### 旅行规划接口

**POST /travel-plan/stream**

创建旅行计划并以流式方式返回内容，适合实现打字机效果。

- 使用 Server-Sent Events (SSE) 格式
- 每个事件包含生成的部分内容
- 当生成完成时发送 `event: complete` 事件

```javascript
// 前端请求示例
const response = await fetch('/travel-plan/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "帮我规划一个为期3天的北京旅行计划"
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const {done, value} = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  // 处理接收到的数据块...
}
```

## 前端集成

### 数据格式

服务返回标准的 Markdown 格式文本，包含以下内容：

- 标题与分节标记
- 行程详情与时间安排
- 景点列表与描述
- 交通与住宿建议
- 费用估算表格
- 注意事项与提示

### 渲染建议

1. **使用 Markdown 渲染库**：如 `marked` (JS), `markdown-it` 等
2. **实现打字机效果**：通过流式响应逐步展示内容
3. **响应式布局**：确保在移动设备上有良好体验
4. **提供复制与导出功能**：支持一键保存旅行计划

### 示例前端实现

```vue
<script setup>
import { ref } from 'vue';
import { marked } from 'marked';

const query = ref('');
const travelContent = ref('');
const loading = ref(false);

const submitQuery = async () => {
  loading.value = true;
  travelContent.value = '';

  const response = await fetch('/travel-plan/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: query.value })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value, { stream: true });
    const lines = chunk.split('\n');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        travelContent.value += line.substring(6) + '\n';
      }
    }
  }
  
  loading.value = false;
};
</script>
```

## 开发指南

### 项目结构

```
travel-plan-service/
├── main.py           # FastAPI 应用入口
├── agent.py          # 旅行规划代理实现
├── mcps.json         # MCP 配置文件
├── requirements.txt  # 项目依赖
└── .env              # 环境变量配置(需创建)
```

### 技术栈

- **Python >= 3.13**
- **FastAPI**: Web框架
- **Langchain**: LLM应用开发框架
- **Uvicorn**: ASGI服务器
- **Python-dotenv**: 环境变量管理
- **Pydantic**: 数据验证

### 扩展与自定义

- **添加新工具**：在 agent.py 中实现新的工具函数
- **调整系统提示**：修改 `mcps.json` 中的系统提示模板
- **自定义响应格式**：在 main.py 中修改响应处理逻辑

## 常见问题

### 处理超时错误

如果遇到请求超时问题，可尝试:
1. 增加 timeout 设置
2. 使用流式 API (`/travel-plan/stream`)
3. 优化提示词，使其更简洁

### 调整生成质量

- 可通过环境变量 `LLM_MODEL` 更换不同模型
- 调整 `mcps.json` 中的系统提示以引导输出格式
- 添加具体的需求和偏好到用户查询中

---

## 许可证

本项目采用 MIT 许可证 进行许可。
