from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.group import Group


async def get_group_by_id(db: AsyncSession, group_id: int, with_students: bool = False) -> Group | None:
    stmt = select(Group).where(Group.id == group_id)
    if with_students:
        stmt = stmt.options(selectinload(Group.students))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_group_by_name(db: AsyncSession, name: str) -> Group | None:
    result = await db.execute(select(Group).where(Group.name == name))
    return result.scalar_one_or_none()


async def list_groups(db: AsyncSession) -> list[Group]:
    result = await db.execute(
        select(Group).options(selectinload(Group.students)).order_by(Group.name)
    )
    return result.scalars().unique().all()


async def create_group(db: AsyncSession, name: str, control_sum: int) -> Group:
    group = Group(name=name, control_sum=control_sum)
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


async def update_group(db: AsyncSession, group: Group, update_data: dict) -> Group:
    for field, value in update_data.items():
        setattr(group, field, value)
    await db.commit()
    await db.refresh(group)
    return group


async def delete_group(db: AsyncSession, group: Group) -> None:
    await db.delete(group)
    await db.commit()


async def count_groups(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(Group.id)))
    return result.scalar_one()


