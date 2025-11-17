from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.group import Student


async def get_student_by_id(db: AsyncSession, student_id: int, with_group: bool = False) -> Student | None:
    stmt = select(Student).where(Student.id == student_id)
    if with_group:
        stmt = stmt.options(selectinload(Student.group))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def list_students(db: AsyncSession) -> list[Student]:
    result = await db.execute(
        select(Student).options(selectinload(Student.group)).order_by(Student.fio)
    )
    return result.scalars().all()


async def create_student(
    db: AsyncSession,
    fio: str,
    group_id: int,
    score_1: str | None = None,
    score_2: str | None = None,
    score_3: str | None = None,
) -> Student:
    student = Student(
        fio=fio,
        group_id=group_id,
        score_1=score_1,
        score_2=score_2,
        score_3=score_3,
    )
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


async def update_student(db: AsyncSession, student: Student, update_data: dict) -> Student:
    for field, value in update_data.items():
        setattr(student, field, value)
    await db.commit()
    await db.refresh(student)
    return student


async def delete_student(db: AsyncSession, student: Student) -> None:
    await db.delete(student)
    await db.commit()


async def count_students(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(Student.id)))
    return result.scalar_one()


