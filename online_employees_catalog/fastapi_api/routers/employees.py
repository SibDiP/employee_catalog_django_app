from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud
from ..database import get_db
from ..schemas import (
    EmployeeListItem,
    EmployeeResponse,
    PaginatedEmployeeResponse,
    TreeNode,
)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=PaginatedEmployeeResponse)
async def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    items = await crud.list_employees(db, skip=skip, limit=limit)
    total = await crud.count_employees(db)
    return PaginatedEmployeeResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
        has_more=skip + len(items) < total,
    )


@router.get("/tree/roots", response_model=list[EmployeeListItem])
async def list_roots(db: AsyncSession = Depends(get_db)):
    return await crud.get_root_employees(db)


@router.get("/{employee_id}/subtree", response_model=list[EmployeeListItem])
async def get_subtree(employee_id: int, db: AsyncSession = Depends(get_db)):
    employee = await crud.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return await crud.get_subtree(db, employee)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    employee = await crud.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee