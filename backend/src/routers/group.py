from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import get_current_user
from src.crud import group as group_crud
from src.database import get_db
from src.schemas.group import GroupCreate, GroupDetailResponse, GroupResponse, GroupUpdate
from src.schemas.student import StudentResponse
from src.utils import student_total_score

router = APIRouter(prefix="/groups", tags=["Groups"])


def _build_group_payload(group, include_students: bool = False) -> dict:
    students = group.students or []
    students_quantity = len(students)
    excluded_students_quantity = sum(
        1
        for student in students
        if group.control_sum > student_total_score(student.score_1, student.score_2, student.score_3)
    )
    payload = {
        "id": group.id,
        "name": group.name,
        "control_sum": group.control_sum,
        "students_quantity": students_quantity,
        "excluded_students_quantity": excluded_students_quantity,
    }
    if include_students:
        payload["students"] = [StudentResponse.model_validate(student) for student in students]
    return payload


@router.post(
    "",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать группу",
)
async def create_group(
    group_create: GroupCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_user),
):
    existing_group = await group_crud.get_group_by_name(db, group_create.name)
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Группа с таким названием уже существует"
        )
    group = await group_crud.create_group(db, group_create.name, group_create.control_sum)
    group = await group_crud.get_group_by_id(db, group.id, with_students=True)
    return _build_group_payload(group)


@router.put(
    "/{group_id}",
    response_model=GroupResponse,
    summary="Изменить группу",
)
async def update_group(
    group_id: int,
    group_update: GroupUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_user),
):
    group = await group_crud.get_group_by_id(db, group_id, with_students=True)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Группа не найдена")

    update_data = group_update.model_dump(exclude_unset=True, exclude_none=True)
    if not update_data:
        return _build_group_payload(group)

    if "name" in update_data:
        existing_group = await group_crud.get_group_by_name(db, update_data["name"])
        if existing_group and existing_group.id != group.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Группа с таким названием уже существует"
            )

    group = await group_crud.update_group(db, group, update_data)
    group = await group_crud.get_group_by_id(db, group.id, with_students=True)
    return _build_group_payload(group)


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить группу",
)
async def delete_group(
    group_id: int,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_user),
):
    group = await group_crud.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Группа не найдена")
    await group_crud.delete_group(db, group)


@router.get(
    "",
    response_model=List[GroupResponse],
    summary="Получить список групп",
)
async def list_groups(
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_user),
):
    groups = await group_crud.list_groups(db)
    return [_build_group_payload(group) for group in groups]


@router.get(
    "/{group_id}",
    response_model=GroupDetailResponse,
    summary="Получить группу",
)
async def get_group(
    group_id: int,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_user),
):
    group = await group_crud.get_group_by_id(db, group_id, with_students=True)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Группа не найдена")
    payload = _build_group_payload(group, include_students=True)
    return payload


