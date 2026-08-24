import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Test Contest Submission API
payload = {
    "session_id": "test-session-123",
    "division": 1,
    "title": "AAPT PhysicsBowl Division 1 Mock Exam",
    "answers": {
        "pb-2025-01": "C", # Correct
        "pb-2025-02": "C", # Correct
        "pb-2025-03": "A"  # Incorrect (Correct is D)
    },
    "time_taken_seconds": 180
}

res = client.post("/api/contest/submit", json=payload)
assert res.status_code == 200, f"Failed: {res.status_code}"
data = res.json()
print("Contest Submission Response:", data)
assert data["score"] == 2, f"Expected score 2, got {data['score']}"
assert data["total"] == 3, f"Expected total 3, got {data['total']}"

# Test Contest Scorecard View
res_view = client.get(f"/contest/results/test-session-123")
assert res_view.status_code == 200, f"Scorecard view failed: {res_view.status_code}"
print("✓ Contest Scorecard View -> 200 OK")

print("\n🎉 CONTEST END-TO-END VERIFICATION PASSED!")
