from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    fio: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    fio: str | None = None
    login: str | None = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(UserInDB):
    pass


class UserMeResponse(UserResponse):
    students_quantity: int
    groups_quantity: int
