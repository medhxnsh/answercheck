from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables
import models  # noqa: F401 — ensure tables are registered


# ── Lifespan ───────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="AnswerCheck API",
    description="AI-powered exam grading backend",
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════
#  ADMIN ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.post("/admin/teachers")
def create_teacher():
    return {"id": 1, "name": "Ms. Sharma"}


@app.get("/admin/teachers")
def list_teachers():
    return [{"id": 1, "name": "Ms. Sharma"}]


@app.post("/admin/classes")
def create_class():
    return {"id": 1, "name": "10A"}


@app.get("/admin/classes")
def list_classes():
    return [{"id": 1, "name": "10A"}]


@app.get("/admin/stats")
def admin_stats():
    return {"exams": 12, "teachers": 4, "classes": 8, "submissions": 45}


# ═══════════════════════════════════════════════════════════════════
#  EXAM ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.post("/exams")
def create_exam():
    return {"id": 1, "title": "Physics Mid Term"}


@app.get("/exams")
def list_exams():
    return [{"id": 1, "title": "Physics Mid Term"}]


@app.get("/exams/active")
def list_active_exams():
    return [{"id": 1, "title": "Physics Mid Term"}]


@app.get("/exams/{id}")
def get_exam(id: int):
    return {"id": id, "title": "Physics Mid Term"}


@app.post("/exams/{id}/answer-key")
def upload_answer_key(id: int):
    return {"status": "uploaded"}


@app.post("/exams/{id}/start")
def start_exam(id: int):
    return {"status": "started", "started_at": "now"}


@app.get("/exams/{id}/timer")
def get_exam_timer(id: int):
    return {"status": "active", "seconds_remaining": 3600}


@app.get("/exams/{id}/classes")
def get_exam_classes(id: int):
    return [{"class_id": 1, "name": "10A", "submitted": 28, "total": 35}]


@app.post("/exams/{id}/submit")
def submit_exam(id: int):
    return {"submission_id": 1, "status": "pending"}


@app.post("/exams/{id}/grade-all/{class_id}")
def grade_all(id: int, class_id: int):
    return {"status": "grading_started"}


@app.post("/exams/{id}/publish")
def publish_exam(id: int):
    return {"status": "published"}


# ═══════════════════════════════════════════════════════════════════
#  SUBMISSION ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.get("/submissions/{id}")
def get_submission(id: int):
    return {
        "id": id,
        "student_name": "Arjun Mehta",
        "status": "graded",
        "total_marks": 34,
        "max_marks": 50,
    }


# ═══════════════════════════════════════════════════════════════════
#  RESULT / DISPUTE ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.post("/results/{qid}/override")
def override_result(qid: int):
    return {"status": "overridden", "marks": 4}


@app.post("/results/{qid}/dispute")
def dispute_result(qid: int):
    return {"status": "flagged"}


@app.get("/disputes")
def list_disputes():
    return [{"id": 1, "reason": "Marks seem low", "status": "pending"}]


@app.patch("/disputes/{id}/resolve")
def resolve_dispute(id: int):
    return {"status": "reviewed"}
