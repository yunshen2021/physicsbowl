import json
import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

def load_formulas():
    file_path = os.path.join(DATA_DIR, "formulas.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

@router.get("/formulas", response_class=HTMLResponse)
async def formula_sheet(request: Request):
    data = load_formulas()
    return templates.TemplateResponse(
        request=request,
        name="formulas/index.html",
        context={
            "constants": data.get("constants", []),
            "categories": data.get("categories", [])
        }
    )
