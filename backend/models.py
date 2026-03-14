from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


# ── Admin ──────────────────────────────────────────────────────────
class Admin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Teacher ────────────────────────────────────────────────────────
class Teacher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    subject: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Class ──────────────────────────────────────────────────────────
class Class(SQLModel, table=True):
    __tablename__ = "class_"  # 'class' is a Python keyword
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    section: Optional[str] = None
    teacher_id: Optional[int] = Field(default=None, foreign_key="teacher.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Exam ───────────────────────────────────────────────────────────
class Exam(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    subject: str
    teacher_id: Optional[int] = Field(default=None, foreign_key="teacher.id")
    class_id: Optional[int] = Field(default=None, foreign_key="class_.id")
    strictness: float = Field(default=0.5)
    timer_type: str = Field(default="duration")  # "fixed" | "duration"
    fixed_deadline: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    started_at: Optional[datetime] = None
    status: str = Field(default="draft")
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── AnswerKey ──────────────────────────────────────────────────────
class AnswerKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exam_id: int = Field(foreign_key="exam.id")
    question_number: int
    max_marks: int = Field(default=5)
    answer_type: str = Field(default="TEXT")  # TEXT | MATH | DIAGRAM
    expected_answer: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Submission ─────────────────────────────────────────────────────
class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exam_id: int = Field(foreign_key="exam.id")
    roll_number: str
    student_name: str
    class_name: str
    section: Optional[str] = None
    exam_date: Optional[str] = None
    sheet_image_path: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending")


# ── QuestionResult ─────────────────────────────────────────────────
class QuestionResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(foreign_key="submission.id")
    question_number: int
    extracted_text: Optional[str] = None
    answer_type: Optional[str] = None
    similarity_score: Optional[float] = None
    ai_marks: Optional[int] = None
    ai_justification: Optional[str] = None
    ai_confidence: Optional[float] = None
    teacher_marks: Optional[int] = None
    final_marks: Optional[int] = None


# ── Dispute ────────────────────────────────────────────────────────
class Dispute(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_result_id: int = Field(foreign_key="questionresult.id")
    roll_number: str
    reason: str
    status: str = Field(default="pending")
    teacher_response: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
