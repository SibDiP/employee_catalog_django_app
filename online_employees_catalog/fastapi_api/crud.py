from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Employee


async def count_employees(db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(Employee))
    return result.scalar_one()


async def list_employees(
    db: AsyncSession,
    skip: int,
    limit: int,
) -> list[Employee]:
    statement = (
        select(Employee)
        .order_by(Employee.path)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(statement)
    return list(result.scalars().all())


async def get_employee(db: AsyncSession, employee_id: int) -> Employee | None:
    result = await db.execute(
        select(Employee).where(Employee.id == employee_id)
    )
    return result.scalar_one_or_none()


async def get_root_employees(db: AsyncSession) -> list[Employee]:
    result = await db.execute(
        select(Employee).where(Employee.depth == 1).order_by(Employee.path)
    )
    return list(result.scalars().all())


async def get_subtree(
    db: AsyncSession,
    employee: Employee,
) -> list[Employee]:
    result = await db.execute(
        select(Employee)
        .where(Employee.path.like(f"{employee.path}%"))
        .order_by(Employee.path)
    )
    return list(result.scalars().all())