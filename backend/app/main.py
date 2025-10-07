from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import AnalyzeRequest, AnalyzeResponse, IssueExplanation
from app.analyzer import analyze_python

app = FastAPI(title="Intelligent Code Review — MVP")

# Enable CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost:5173"] for stricter
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    res = analyze_python(req.filename, req.content)
    issues = [
        IssueExplanation(
            title=i["title"],
            category=i["category"],
            severity=i["severity"],
            lineno=i["lineno"],
            snippet=i["snippet"],
            why=i["why"],
            fix=i["fix"],
            principle=i["principle"],
        )
        for i in res["issues"]
    ]
    return AnalyzeResponse(
        filename=res["filename"],
        issues=issues,
        metrics=res["metrics"],
        score=res["score"],
    )
