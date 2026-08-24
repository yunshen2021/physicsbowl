import sys
import os
import uvicorn
import webbrowser
import threading
import time

# Ensure project root is in python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app.database import init_db

def open_browser():
    time.sleep(1.2)
    print("\n🚀 Opening PhysicsBowl Arena in your web browser: http://127.0.0.1:8000\n")
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        pass

def main():
    print("=" * 65)
    print(" ⚡ PhysicsBowl Arena (PhysCode) - AAPT Competition Training")
    print("=" * 65)
    
    # 1. Initialize Postgres schema (tables created if missing)
    init_db()
    print("✓ Database schema initialized")

    # 2. Launch browser automatically in background
    threading.Thread(target=open_browser, daemon=True).start()

    # 3. Start Uvicorn Server
    print("✓ Starting server at http://127.0.0.1:8000 (Press Ctrl+C to stop)")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
