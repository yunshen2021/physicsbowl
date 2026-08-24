import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import init_db, record_submission, get_all_question_statuses
from app.main import app
from fastapi.testclient import TestClient

print("1. Initializing DB...")
init_db()
print("   ✓ DB initialized successfully.")

print("2. Testing TestClient endpoints...")
client = TestClient(app)

# Test GET /
res = client.get("/")
assert res.status_code == 200, f"GET / failed: {res.status_code}"
print("   ✓ GET / (Dashboard) -> 200 OK")

# Test GET /problems
res = client.get("/problems")
assert res.status_code == 200, f"GET /problems failed: {res.status_code}"
print("   ✓ GET /problems -> 200 OK")

# Test GET /problems with year filter
res = client.get("/problems?year=2025")
assert res.status_code == 200, f"GET /problems?year=2025 failed: {res.status_code}"
assert "2025" in res.text
print("   ✓ GET /problems?year=2025 -> 200 OK")

# Test GET /problems/pb-2025-01
res = client.get("/problems/pb-2025-01")
assert res.status_code == 200, f"GET /problems/pb-2025-01 failed: {res.status_code}"
print("   ✓ GET /problems/pb-2025-01 -> 200 OK")

# Test POST /api/problems/pb-2025-01/submit
res = client.post("/api/problems/pb-2025-01/submit", json={"selected_option": "C", "time_spent_seconds": 35})
assert res.status_code == 200, f"Submit failed: {res.status_code}"
data = res.json()
assert data["is_correct"] == True, f"Expected correct answer C: {data}"
print("   ✓ POST /api/problems/pb-2025-01/submit (Correct: C) -> 200 OK, Accepted!")

# Test GET /contest
res = client.get("/contest")
assert res.status_code == 200, f"GET /contest failed: {res.status_code}"
print("   ✓ GET /contest (Hub) -> 200 OK")

# Test GET /contest/div1-mock
res = client.get("/contest/div1-mock")
assert res.status_code == 200, f"GET /contest/div1-mock failed: {res.status_code}"
print("   ✓ GET /contest/div1-mock -> 200 OK")

# Test GET /contest/pb-2025-div1 (Official 2025 Division 1 Exam)
res = client.get("/contest/pb-2025-div1")
assert res.status_code == 200, f"GET /contest/pb-2025-div1 failed: {res.status_code}"
print("   ✓ GET /contest/pb-2025-div1 (Official 2025 Div 1) -> 200 OK")

# Test GET /contest/pb-2025-div2 (Official 2025 Division 2 Exam)
res = client.get("/contest/pb-2025-div2")
assert res.status_code == 200, f"GET /contest/pb-2025-div2 failed: {res.status_code}"
print("   ✓ GET /contest/pb-2025-div2 (Official 2025 Div 2) -> 200 OK")

# Test GET /formulas
res = client.get("/formulas")
assert res.status_code == 200, f"GET /formulas failed: {res.status_code}"
print("   ✓ GET /formulas -> 200 OK")

print("\n🎉 ALL 895-QUESTION APP TESTS PASSED SUCCESSFULLY!")
