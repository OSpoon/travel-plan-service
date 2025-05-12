import os
import json
from fastapi import FastAPI, Query, Response
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


@app.get("/travel-plan/stream")
async def travel_plan_stream(query: str = Query(default="")):
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
                if content:
                    yield {
                        "event": "message",
                        "data": json.dumps({"content": content}, ensure_ascii=False),
                    }

            # 发送完成事件
            yield {"event": "complete", "data": "规划完成"}
        except Exception as e:
            yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
