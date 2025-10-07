from pydantic import BaseModel
from typing import List

class AnalyzeRequest(BaseModel):
    filename: str
    content: str

class IssueExplanation(BaseModel):
    title: str
    category: str
    severity: str
    lineno: int
    snippet: str
    why: str
    fix: str
    principle: str

class AnalyzeResponse(BaseModel):
    filename: str
    issues: List[IssueExplanation]
    metrics: dict
    score: dict
