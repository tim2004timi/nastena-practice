from pydantic import BaseModel

from src.schemas.student import StudentResponse


class GroupBase(BaseModel):
    name: str
    control_sum: int


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: str | None = None
    control_sum: int | None = None


class GroupResponse(GroupBase):
    id: int
    students_quantity: int
    excluded_students_quantity: int

    class Config:
        from_attributes = True


class GroupDetailResponse(GroupResponse):
    students: list[StudentResponse]


