import json
import os
import random
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    record_submission,
    get_question_status,
    get_all_question_statuses,
    toggle_bookmark,
    is_bookmarked,
    save_note,
    get_note
)
from app.models import SubmitRequest, NoteRequest

router = APIRouter()

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Official AAPT PhysicsBowl exam PDFs (each includes that year's equation
# sheet on its cover pages). Verified reachable (HTTP 200) for every year
# present in questions.json.
AAPT_EXAM_LINKS = {
    2007: "https://www.aapt.org/programs/physicsbowl/upload/PhysicsBowl_2007.pdf",
    2008: "https://www.aapt.org/Programs/PhysicsBowl/upload/PhysicsBowl_2008_Exam.pdf",
    2009: "https://www.aapt.org/Programs/PhysicsBowl/upload/PhysicsBowl_2009_Exam.pdf",
    2010: "https://www.aapt.org/programs/physicsbowl/upload/PhysicsBowl_2010.pdf",
    2011: "https://www.aapt.org/programs/physicsbowl/upload/PhysicsBowl_2011.pdf",
    2012: "https://www.aapt.org/programs/physicsbowl/upload/PhysicsBowl_2012.pdf",
    2013: "https://www.aapt.org/programs/physicsbowl/upload/PhysicsBowl_2013.pdf",
    2014: "https://www.aapt.org/Programs/PhysicsBowl/upload/PhysicsBowl_2014_Exam.pdf",
    2015: "https://www.aapt.org/Programs/PhysicsBowl/upload/2015-PhysicsBowl-Final.pdf",
    2016: "https://www.aapt.org/Programs/PhysicsBowl/upload/PhysicsBowl_2016.pdf",
    2017: "https://www.aapt.org/Programs/PhysicsBowl/upload/PhysicsBowl_2017.pdf",
    2018: "https://www.aapt.org/Programs/PhysicsBowl/upload/2018-PhysicsBowl-Exam-2.pdf",
    2019: "https://www.aapt.org/Programs/PhysicsBowl/upload/2019-PhysicsBowl-Exam.pdf",
    2021: "https://www.aapt.org/Programs/PhysicsBowl/upload/2021-PhysicsBowl-Exam-2.pdf",
    2022: "https://www.aapt.org/Programs/PhysicsBowl/upload/PB-Exam-2022-2.pdf",
    2023: "https://www.aapt.org/Programs/PhysicsBowl/upload/PB-Exam-Draft-J-2023-2.pdf",
    2024: "https://www.aapt.org/Programs/PhysicsBowl/upload/PB-Exam-Draft-I-Final-version-2024.pdf",
    2025: "https://www.aapt.org/Programs/PhysicsBowl/upload/PB-Exam-25-2.pdf",
}

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

@router.get("/problems", response_class=HTMLResponse)
async def list_problems(
    request: Request,
    year: str = "all",
    division: str = "all",
    topic: str = "all",
    difficulty: str = "all",
    status: str = "all",
    search: str = ""
):
    all_q = load_questions()
    user_statuses = get_all_question_statuses()

    filtered = []
    topics = sorted(list(set(q["topic"] for q in all_q)))
    years = sorted(list(set(q.get("year", 2025) for q in all_q if q.get("year"))), reverse=True)

    for q in all_q:
        q_status = user_statuses.get(q["id"], "unsolved")
        q["user_status"] = q_status
        q["is_bookmarked"] = is_bookmarked(q["id"])

        # Filter by Year
        if year != "all":
            try:
                y_int = int(year)
                if q.get("year") != y_int:
                    continue
            except ValueError:
                pass

        # Filter by Division
        if division != "all":
            if division == "1" and q["division"] not in [1, "both"]:
                continue
            if division == "2" and q["division"] not in [2, "both"]:
                continue

        # Filter by Topic
        if topic != "all" and q["topic"].lower() != topic.lower():
            continue

        # Filter by Difficulty
        if difficulty != "all" and q["difficulty"].lower() != difficulty.lower():
            continue

        # Filter by Status
        if status != "all":
            if status == "solved" and q_status != "solved":
                continue
            if status == "attempted" and q_status != "attempted":
                continue
            if status == "unsolved" and q_status != "unsolved":
                continue

        # Search Query
        if search:
            s = search.lower()
            if s not in q["title"].lower() and s not in q["content"].lower() and s not in q["topic"].lower():
                continue

        filtered.append(q)

    # Calculate overall stats
    total_count = len(all_q)
    solved_count = sum(1 for q in all_q if user_statuses.get(q["id"]) == "solved")
    attempted_count = sum(1 for q in all_q if user_statuses.get(q["id"]) == "attempted")

    return templates.TemplateResponse(
        request=request,
        name="problems/list.html",
        context={
            "problems": filtered,
            "topics": topics,
            "years": years,
            "current_year": year,
            "current_division": division,
            "current_topic": topic,
            "current_difficulty": difficulty,
            "current_status": status,
            "current_search": search,
            "total_count": total_count,
            "solved_count": solved_count,
            "attempted_count": attempted_count
        }
    )

@router.get("/problems/{problem_id}", response_class=HTMLResponse)
async def problem_arena(request: Request, problem_id: str):
    all_q = load_questions()
    question = next((q for q in all_q if q["id"] == problem_id), None)
    
    if not question:
        raise HTTPException(status_code=404, detail="Problem not found")

    status = get_question_status(problem_id)
    bookmarked = is_bookmarked(problem_id)
    user_note = get_note(problem_id)
    formulas_data = load_formulas()

    # Find previous and next problem IDs
    q_index = next(i for i, q in enumerate(all_q) if q["id"] == problem_id)
    prev_id = all_q[q_index - 1]["id"] if q_index > 0 else None
    next_id = all_q[q_index + 1]["id"] if q_index < len(all_q) - 1 else None

    return templates.TemplateResponse(
        request=request,
        name="problems/arena.html",
        context={
            "question": question,
            "question_json": json.dumps(question),
            "status": status,
            "is_bookmarked": bookmarked,
            "user_note": user_note,
            "prev_id": prev_id,
            "next_id": next_id,
            "formulas_data": formulas_data,
            "total_problems": len(all_q),
            "problem_number": q_index + 1,
            "aapt_exam_link": AAPT_EXAM_LINKS.get(question.get("year"))
        }
    )

@router.post("/api/problems/{problem_id}/submit")
async def submit_answer(problem_id: str, payload: SubmitRequest):
    all_q = load_questions()
    question = next((q for q in all_q if q["id"] == problem_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Problem not found")

    is_correct = (payload.selected_option.upper() == question["correctAnswer"].upper())
    record_submission(
        question_id=problem_id,
        selected_option=payload.selected_option.upper(),
        is_correct=is_correct,
        time_spent_seconds=payload.time_spent_seconds
    )

    return JSONResponse({
        "success": True,
        "is_correct": is_correct,
        "selected_option": payload.selected_option.upper(),
        "correct_answer": question["correctAnswer"],
        "solution": question["solution"]
    })

@router.post("/api/problems/{problem_id}/bookmark")
async def bookmark_endpoint(problem_id: str):
    new_state = toggle_bookmark(problem_id)
    return JSONResponse({"bookmarked": new_state})

@router.post("/api/problems/{problem_id}/note")
async def save_note_endpoint(problem_id: str, payload: NoteRequest):
    save_note(problem_id, payload.content)
    return JSONResponse({"success": True})

@router.get("/api/problems/random")
async def get_random_problem():
    all_q = load_questions()
    if not all_q:
        raise HTTPException(status_code=404, detail="No problems available")
    chosen = random.choice(all_q)
    return JSONResponse({"problem_id": chosen["id"]})
