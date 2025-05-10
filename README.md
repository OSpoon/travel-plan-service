# Travel Plan Service 旅行规划服务

## 项目简介

这是一个基于AI的旅行规划服务，能够根据用户的具体需求，自动生成个性化的旅行攻略。该服务使用FastAPI构建RESTful API，集成了先进的语言模型来提供智能化的旅行规划建议。

## 功能特点

- 智能旅行规划：根据用户输入自动生成定制化旅行方案
- RESTful API：提供简单易用的HTTP接口
- 灵活配置：支持自定义语言模型参数
- 环境变量支持：通过.env文件安全管理配置

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