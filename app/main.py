import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routers import problems, contests, formulas, stats

app = FastAPI(
    title="PhysicsBowl Arena (PhysCode)",
    description="A LeetCode-style local platform for AAPT PhysicsBowl competition training",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Mount static files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include Routers
app.include_router(stats.router)
app.include_router(problems.router)
app.include_router(contests.router)
app.include_router(formulas.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
