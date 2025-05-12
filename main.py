import os
import json
from fastapi import FastAPI, Body, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from agent import TravelPlanAgent

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
async def travel_plan_stream(query: str = Body(..., embed=True)):
    if not query.strip():
        return Response(
            content=json.dumps({"error": "查询参数不能为空"}),
            media_type="application/json",
        )

    async def content_generator():
        try:
            async for content in travel_agent.astream(
                query=query,
                model=os.getenv("LLM_MODEL", ""),
                base_url=os.getenv("LLM_BASE_URL", ""),
                api_key=os.getenv("LLM_API_KEY", ""),
            ):
                if content:
                    yield json.dumps({"content": content}, ensure_ascii=False) + "\n"
            
            # 发送完成标记
            yield json.dumps({"status": "complete"}, ensure_ascii=False)
        except Exception as e:
            yield json.dumps({"error": str(e)}, ensure_ascii=False)

    return StreamingResponse(
        content_generator(),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
