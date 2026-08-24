import json
import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    save_contest_result,
    get_contest_result,
    get_recent_contests,
    record_submission
)
from app.models import ContestSubmitRequest

router = APIRouter()

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

def load_questions():
    file_path = os.path.join(DATA_DIR, "questions.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def load_formulas():
    file_path = os.path.join(DATA_DIR, "formulas.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

CONTEST_PRESETS = {
    "div1-mock": {
        "id": "div1-mock",
        "title": "AAPT PhysicsBowl Division 1 Mock Exam",
        "division": 1,
        "description": "Standard 45-minute timed competition for first-year physics students. Covers kinematics, dynamics, energy, basic E&M, and optics.",
        "duration_minutes": 45,
        "question_count": 40
    },
    "div2-mock": {
        "id": "div2-mock",
        "title": "AAPT PhysicsBowl Division 2 Mock Exam",
        "division": 2,
        "description": "Challenging 45-minute timed competition for advanced physics students. Includes rotational mechanics, relativity, thermodynamics, and modern physics.",
        "duration_minutes": 45,
        "question_count": 40
    },
    "sprint-drill": {
        "id": "sprint-drill",
        "title": "PhysicsBowl Rapid Fire Sprint",
        "division": 1,
        "description": "Fast-paced 12-minute practice sprint with 10 questions to test speed and formula recall.",
        "duration_minutes": 12,
        "question_count": 10
    }
}

@router.get("/contest", response_class=HTMLResponse)
async def contest_hub(request: Request):
    recent_contests = get_recent_contests()
    return templates.TemplateResponse(
        request=request,
        name="contest/hub.html",
        context={
            "presets": CONTEST_PRESETS,
            "recent_contests": recent_contests
        }
    )

@router.get("/contest/{contest_type}", response_class=HTMLResponse)
async def contest_runner(request: Request, contest_type: str):
    preset = CONTEST_PRESETS.get(contest_type)
    if not preset:
        raise HTTPException(status_code=404, detail="Contest preset not found")

    all_q = load_questions()
    div = preset["division"]
    
    # Filter questions matching division or both
    matching_q = [q for q in all_q if q["division"] in [div, "both"]]
    
    # If not enough, take available questions
    if len(matching_q) < preset["question_count"]:
        contest_q = matching_q if matching_q else all_q
    else:
        contest_q = matching_q[:preset["question_count"]]

    formulas_data = load_formulas()
    session_id = str(uuid.uuid4())

    return templates.TemplateResponse(
        request=request,
        name="contest/runner.html",
        context={
            "preset": preset,
            "questions": contest_q,
            "questions_json": json.dumps(contest_q),
            "formulas_data": formulas_data,
            "session_id": session_id,
            "duration_seconds": preset["duration_minutes"] * 60
        }
    )

@router.post("/api/contest/submit")
async def submit_contest(payload: ContestSubmitRequest):
    all_q = load_questions()
    q_map = {q["id"]: q for q in all_q}

    score = 0
    total = len(payload.answers)
    topic_stats = {}
    details = []

    for q_id, chosen_option in payload.answers.items():
        q = q_map.get(q_id)
        if not q:
            continue

        topic = q.get("topic", "General")
        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "total": 0}
        topic_stats[topic]["total"] += 1

        is_corr = (chosen_option.upper() == q["correctAnswer"].upper())
        if is_corr:
            score += 1
            topic_stats[topic]["correct"] += 1

        record_submission(
            question_id=q_id,
            selected_option=chosen_option.upper(),
            is_correct=is_corr,
            time_spent_seconds=max(1, payload.time_taken_seconds // max(1, total))
        )

        details.append({
            "question_id": q_id,
            "title": q["title"],
            "topic": topic,
            "selected_option": chosen_option.upper(),
            "correct_answer": q["correctAnswer"],
            "is_correct": is_corr,
            "solution": q["solution"]
        })

    ratio = score / total if total > 0 else 0
    if ratio >= 0.85:
        percentile = 98
    elif ratio >= 0.70:
        percentile = 90
    elif ratio >= 0.55:
        percentile = 75
    elif ratio >= 0.40:
        percentile = 50
    elif ratio >= 0.25:
        percentile = 30
    else:
        percentile = 15

    answers_payload = {
        "details": details,
        "topic_stats": topic_stats,
        "percentile": percentile
    }

    save_contest_result(
        session_id=payload.session_id,
        title=payload.title,
        division=payload.division,
        score=score,
        total=total,
        time_taken=payload.time_taken_seconds,
        answers_json=json.dumps(answers_payload)
    )

    return JSONResponse({
        "success": True,
        "session_id": payload.session_id,
        "score": score,
        "total": total,
        "redirect_url": f"/contest/results/{payload.session_id}"
    })

@router.get("/contest/results/{session_id}", response_class=HTMLResponse)
async def contest_results(request: Request, session_id: str):
    res = get_contest_result(session_id)
    if not res:
        raise HTTPException(status_code=404, detail="Contest result not found")

    answers_data = json.loads(res["answers_json"])
    
    return templates.TemplateResponse(
        request=request,
        name="contest/results.html",
        context={
            "session": dict(res),
            "details": answers_data.get("details", []),
            "topic_stats": answers_data.get("topic_stats", {}),
            "percentile": answers_data.get("percentile", 50)
        }
    )
