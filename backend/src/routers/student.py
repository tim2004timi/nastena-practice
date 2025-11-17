from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import get_current_user
from src.crud import group as group_crud
from src.crud import student as student_crud
from src.database import get_db
from src.schemas.student import StudentCreate, StudentResponse, StudentUpdate, StudentWithGroupResponse

router = APIRouter(prefix="/students", tags=["Students"])


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить студента",
)
async def create_student(
    student_create: StudentCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_user),
):
    """Создать нового студента (требуется только ФИО и номер группы)"""
    # Проверяем существование группы
    group = await group_crud.get_group_by_id(db, student_create.group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Группа не найдена")

    student = await student_crud.create_student(
        db=db,
        fio=student_create.fio,
        group_id=student_create.group_id,
        score_1=student_create.score_1,
        score_2=student_create.score_2,
        score_3=student_create.score_3,
    )
    return StudentResponse.model_validate(student)


@router.get(
    "",
    response_model=List[StudentWithGroupResponse],
    summary="Получить список студентов",
)
async def list_students(
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_user),
):
    students = await student_crud.list_students(db)
    return [
        StudentWithGroupResponse(
            id=student.id,
            fio=student.fio,
            score_1=student.score_1,
            score_2=student.score_2,
            score_3=student.score_3,
            group_id=student.group_id,
            group_name=student.group.name if student.group else None,
        )
        for student in students
    ]


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Изменить студента",
)
async def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_user),
):
    student = await student_crud.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")

    update_data = student_update.model_dump(exclude_unset=True)
    if "group_id" in update_data:
        new_group = await group_crud.get_group_by_id(db, update_data["group_id"])
        if not new_group:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Группа не найдена")

    if not update_data:
        return StudentResponse.model_validate(student)

    student = await student_crud.update_student(db, student, update_data)
    return StudentResponse.model_validate(student)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить студента",
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_user),
):
    student = await student_crud.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    await student_crud.delete_student(db, student)


