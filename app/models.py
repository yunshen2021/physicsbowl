from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Option(BaseModel):
    id: str
    text: str

class Solution(BaseModel):
    summary: str
    steps: List[str]
    formulasUsed: List[str]
    keyTakeaway: str

class Question(BaseModel):
    id: str
    question_number: Optional[int] = None
    title: str
    division: Any  # 1, 2, or "both"
    topic: str
    difficulty: str
    acceptance_rate: str
    year: Optional[int] = 2025
    content: str
    diagramSvg: Optional[str] = None
    options: List[Option]
    correctAnswer: str
    hints: List[str] = []
    solution: Solution

class SubmitRequest(BaseModel):
    selected_option: str
    time_spent_seconds: int = 0

class ContestSubmitRequest(BaseModel):
    session_id: str
    division: int
    title: str
    answers: Dict[str, str] # question_id -> selected_option
    time_taken_seconds: int

class NoteRequest(BaseModel):
    content: str
