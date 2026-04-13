from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from graph.workflow import build_graph
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Research Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


class QuestionRequest(BaseModel):
    question: str


class ResearchResponse(BaseModel):
    question: str
    answer: str
    revisions: int


@app.post("/research", response_model=ResearchResponse)
async def research(request: QuestionRequest):
    initial_state = {
        "question": request.question,
        "sub_questions": [],
        "search_results": [],
        "draft_answer": "",
        "critique": "",
        "revision_count": 0,
        "is_satisfactory": False,
        "final_answer": ""
    }

    try:
        result = await graph.ainvoke(initial_state)
        return ResearchResponse(
            question=request.question,
            answer=result["final_answer"],
            revisions=result["revision_count"]
        )
    except Exception as e:
        logger.error(f"Error during research: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
