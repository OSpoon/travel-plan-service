# Travel Plan Service 旅行规划服务

## 项目简介

这是一个基于AI的旅行规划服务，能够根据用户的具体需求，自动生成个性化的旅行攻略。该服务使用FastAPI构建RESTful API，集成了先进的语言模型来提供智能化的旅行规划建议。

## 功能特点

- 智能旅行规划：根据用户输入自动生成定制化旅行方案
- RESTful API：提供简单易用的HTTP接口
- 灵活配置：支持自定义语言模型参数
- 环境变量支持：通过.env文件安全管理配置
- 流式输出：支持实时流式返回AI生成内容

## 数据格式说明

### 消息格式

服务端返回的每条消息都是JSON格式，包含以下字段：

```json
{
  "type": "AIMessage | FunctionMessage",  // 消息类型
  "content": "消息内容",                 // Markdown格式的文本内容
  "name": "工具名称",                    // 仅在FunctionMessage类型时存在
  "tool_calls": [                        // 工具调用信息（可选）
    {
      "name": "工具名称",
      "arguments": "工具参数"
    }
  ]
}
```

### 消息类型说明

1. AIMessage
   - 表示AI助手的回复消息
   - content字段包含Markdown格式的文本
   - 可能包含tool_calls字段，表示需要调用的工具

2. FunctionMessage
   - 表示工具调用的结果
   - name字段指示工具名称
   - content字段包含工具返回的结果

### 前端渲染建议

1. 内容渲染
   - 使用Markdown渲染库处理content字段
   - 支持标题、列表、表格等Markdown语法
   - 保留原始格式和换行

2. 工具调用处理
   - 解析tool_calls数组中的工具调用信息
   - 针对特定工具（如地图导航）提供可视化展示
   - 支持异步加载工具调用结果

3. 流式更新
   - 实现打字机效果的渲染
   - 支持内容块的动态追加
   - 处理不同类型消息的平滑过渡

### 示例代码

```javascript
// 前端流式处理示例
const processStream = async (response) => {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  
  while (true) {
    const {value, done} = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, {stream: true});
    const lines = buffer.split("\n");
    buffer = lines.pop();
    
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const data = JSON.parse(line.slice(6));
        if (data.content) {
          // 渲染Markdown内容
          renderMarkdown(data.content);
        }
        if (data.additional_kwargs?.tool_calls) {
          // 处理工具调用
          handleToolCalls(data.additional_kwargs.tool_calls);
        }
      }
    }
  }
};

// Markdown渲染函数
const renderMarkdown = (content) => {
  const html = marked(content); // 使用marked等Markdown库
  appendToOutput(html);
};

// 工具调用处理函数
const handleToolCalls = (toolCalls) => {
  toolCalls.forEach(call => {
    switch(call.function.name) {
      case 'maps_direction_driving':
        renderMap(JSON.parse(call.function.arguments));
        break;
      // 处理其他工具调用
    }
  });
};
```

## 技术栈

- Python >= 3.13
- FastAPI
- Langchain
- Uvicorn
- Python-dotenv
- Pydantic

## 安装说明

1. 克隆项目到本地：
```bash
git clone [repository-url]
cd travel-plan-service
```

2. 安装依赖：
```bash
pip install -e .
```

3. 配置环境变量：
   - 复制`.env.example`文件并重命名为`.env`
   - 在`.env`文件中填入必要的配置信息：
```env
LLM_MODEL=your_model_name
LLM_BASE_URL=your_base_url
LLM_API_KEY=your_api_key

AMAP_KEY=your_amap_key
```

## 使用方法

1. 启动服务：
```bash
python main.py
```
服务将在 http://localhost:8000 启动

2. API调用示例：

```python
import requests

url = "http://localhost:8000/travel-plan"
data = {
    "query": "帮我规划一个为期3天的北京旅行计划"
}

response = requests.post(url, json=data)
print(response.json())
```

## API文档

### POST /travel-plan

创建旅行计划

**请求体：**

```json
{
    "query": "string",              // 必填，旅行需求描述
    "model": "string",             // 可选，语言模型名称
    "base_url": "string",          // 可选，模型API基础URL
    "api_key": "string"           // 可选，API密钥
}
```

**响应：**

```json
{
    "plan": "string"               // 生成的旅行计划
}
```

### POST /travel-plan/stream

创建旅行计划（流式输出）

**请求体：**

与 `/travel-plan` 接口相同

**响应：**

返回 Server-Sent Events (SSE) 流，每个事件包含生成的旅行计划的部分内容。

**使用示例：**

```python
import requests

def stream_response(url, data):
    with requests.post(url, json=data, stream=True) as response:
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                print(chunk, end="", flush=True)

url = "http://localhost:8000/travel-plan/stream"
data = {
    "query": "帮我规划一个为期3天的北京旅行计划"
}

stream_response(url, data)
```

## 开发说明

- `main.py`: FastAPI应用程序入口
- `agent.py`: 旅行规划代理实现
- `mcps.json`: MCP配置文件
- `.env`: 环境变量配置

## 注意事项

- 确保已正确配置所有必要的环境变量
- API密钥等敏感信息请妥善保管，不要提交到版本控制系统
- 建议在生产环境中使用适当的安全措施保护API端点

## 许可证

MIT License