from pydantic import BaseModel, field_validator

from src.utils import ALLOWED_STUDENT_SCORES


class StudentBase(BaseModel):
    fio: str
    score_1: str | None = None
    score_2: str | None = None
    score_3: str | None = None

    @field_validator("score_1", "score_2", "score_3")
    @classmethod
    def validate_score(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned_value = value.strip()
        if cleaned_value not in ALLOWED_STUDENT_SCORES:
            raise ValueError(f"Оценка должна быть в {ALLOWED_STUDENT_SCORES}")
        return cleaned_value


class StudentCreate(StudentBase):
    group_id: int


class StudentUpdate(BaseModel):
    fio: str | None = None
    score_1: str | None = None
    score_2: str | None = None
    score_3: str | None = None
    group_id: int | None = None

    @field_validator("score_1", "score_2", "score_3")
    @classmethod
    def validate_score(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned_value = value.strip()
        if cleaned_value not in ALLOWED_STUDENT_SCORES:
            raise ValueError(f"Оценка должна быть в {ALLOWED_STUDENT_SCORES}")
        return cleaned_value


class StudentResponse(StudentBase):
    id: int
    group_id: int

    class Config:
        from_attributes = True


class StudentWithGroupResponse(StudentResponse):
    group_name: str | None = None


