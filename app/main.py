from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agents.research_graph import research_graph

app = FastAPI(
    title="Autonomous Multi-Agent Enterprise Research Engine",
    description="Asynchronous LangGraph multi-agent pipeline for automated research synthesis.",
    version="1.0.0"
)

# CORS allow karein taaki browser Swagger UI se request block na kare
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    topic: str
    report: str
    status: str

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Autonomous Research Engine"}

@app.post("/api/v1/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Research topic cannot be empty.")
    
    initial_state = {
        "topic": request.topic,
        "search_results": [],
        "report": "",
        "status": "Initiated"
    }
    
    result = research_graph.invoke(initial_state)
    
    return ResearchResponse(
        topic=result["topic"],
        report=result["report"],
        status=result["status"]
    )