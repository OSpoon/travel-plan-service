import os
import json
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from agent import TravelPlanAgent
from sse_starlette.sse import EventSourceResponse

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

travel_agent = TravelPlanAgent()


@app.post("/travel-plan/stream")
async def travel_plan_stream(request: Request):
    # 从请求体获取query
    data = await request.json()
    query = data.get("query", "")

    if not query.strip():
        return Response(
            content=json.dumps({"error": "查询参数不能为空"}),
            media_type="application/json",
        )

    async def event_generator():
        try:
            async for content in travel_agent.astream(
                query=query,
                model=os.getenv("LLM_MODEL", ""),
                base_url=os.getenv("LLM_BASE_URL", ""),
                api_key=os.getenv("LLM_API_KEY", ""),
            ):
                # 返回SSE格式的消息
                yield {
                    "event": "message",
                    "data": content,
                }

            # 发送完成事件
            yield {"event": "complete"}
        except Exception as e:
            print(f"Stream error: {e}")
            yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
