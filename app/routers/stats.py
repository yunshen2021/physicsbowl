import json
import os
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db, get_submission_history_daily, get_recent_contests, get_all_question_statuses

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

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    all_q = load_questions()
    statuses = get_all_question_statuses()
    
    total_problems = len(all_q)
    solved_problems = sum(1 for q in all_q if statuses.get(q["id"]) == "solved")
    attempted_problems = sum(1 for q in all_q if statuses.get(q["id"]) == "attempted")
    
    # Topic breakdown
    topic_map = {}
    for q in all_q:
        top = q["topic"]
        if top not in topic_map:
            topic_map[top] = {"total": 0, "solved": 0}
        topic_map[top]["total"] += 1
        if statuses.get(q["id"]) == "solved":
            topic_map[top]["solved"] += 1

    # Difficulty breakdown
    diff_map = {
        "Easy": {"total": 0, "solved": 0},
        "Medium": {"total": 0, "solved": 0},
        "Hard": {"total": 0, "solved": 0}
    }
    for q in all_q:
        d = q.get("difficulty", "Medium")
        if d in diff_map:
            diff_map[d]["total"] += 1
            if statuses.get(q["id"]) == "solved":
                diff_map[d]["solved"] += 1

    # Calculate streak from submission history
    daily_history = get_submission_history_daily()
    history_dict = {r["sub_date"]: r["count"] for r in daily_history}

    streak = 0
    today = date.today()
    cur_day = today
    
    # If today has activity or check back from yesterday
    if today.isoformat() in history_dict:
        streak += 1
        cur_day = today - timedelta(days=1)
    else:
        # Check if yesterday had submissions
        yesterday = today - timedelta(days=1)
        if yesterday.isoformat() in history_dict:
            cur_day = yesterday

    while cur_day.isoformat() in history_dict and history_dict[cur_day.isoformat()] > 0:
        streak += 1
        cur_day -= timedelta(days=1)

    # 60-day heatmap data
    heatmap_days = []
    for i in range(60, -1, -1):
        d = today - timedelta(days=i)
        d_str = d.isoformat()
        count = history_dict.get(d_str, 0)
        heatmap_days.append({
            "date": d_str,
            "day_name": d.strftime("%a"),
            "count": count,
            "level": min(4, count) if count > 0 else 0
        })

    recent_contests = get_recent_contests()

    # Recent submissions
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, question_id, selected_option, is_correct, time_spent_seconds, created_at
            FROM submissions
            ORDER BY created_at DESC
            LIMIT 5
        """)
        raw_subs = cursor.fetchall()
        recent_submissions = []
        q_lookup = {q["id"]: q["title"] for q in all_q}
        for s in raw_subs:
            sub_dict = dict(s)
            sub_dict["title"] = q_lookup.get(sub_dict["question_id"], sub_dict["question_id"])
            recent_submissions.append(sub_dict)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "total_problems": total_problems,
            "solved_problems": solved_problems,
            "attempted_problems": attempted_problems,
            "topic_map": topic_map,
            "topic_map_json": json.dumps(topic_map),
            "diff_map": diff_map,
            "streak": streak,
            "heatmap_days": heatmap_days,
            "recent_contests": recent_contests,
            "recent_submissions": recent_submissions
        }
    )

@router.get("/api/stats")
async def get_stats_api():
    daily_history = get_submission_history_daily()
    return JSONResponse({
        "daily_history": [dict(r) for r in daily_history]
    })
