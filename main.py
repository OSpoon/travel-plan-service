import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from agent import TravelPlanAgent

load_dotenv()

app = FastAPI(
    title="Travel Plan Service", description="旅行规划服务API", version="0.1.0"
)


class TravelPlanRequest(BaseModel):
    query: str
    model: Optional[str] = None
    base_url: Optional[str] = None
    api_key: Optional[str] = None


class TravelPlanResponse(BaseModel):
    plan: str


@app.post("/travel-plan", response_model=TravelPlanResponse)
async def create_travel_plan(request: TravelPlanRequest):
    try:
        agent = TravelPlanAgent()
        result = await agent.execute(
            query=request.query,
            model=request.model or os.getenv("LLM_MODEL", ""),
            base_url=request.base_url or os.getenv("LLM_BASE_URL", ""),
            api_key=request.api_key or os.getenv("LLM_API_KEY", ""),
        )
        return TravelPlanResponse(plan=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
