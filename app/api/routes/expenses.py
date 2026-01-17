from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.db import models
from app.schemas import expense as expense_schemas

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=expense_schemas.ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_in: expense_schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_expense = models.Expense(
        user_id=current_user.id,
        amount=expense_in.amount,
        category=expense_in.category,
        description=expense_in.description,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/", response_model=List[expense_schemas.ExpenseOut])
def list_expenses(
    period: Optional[str] = Query(
        default=None,
        description="week, month, 3months, or custom"
    ),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = (
        db.query(models.Expense)
        .filter(models.Expense.user_id == current_user.id)
    )

    now = datetime.utcnow()

    if period == "week":
        since = now - timedelta(weeks=1)
        query = query.filter(models.Expense.created_at >= since)
    elif period == "month":
        since = now - timedelta(days=30)
        query = query.filter(models.Expense.created_at >= since)
    elif period == "3months":
        since = now - timedelta(days=90)
        query = query.filter(models.Expense.created_at >= since)
    elif period == "custom":
        if not start_date or not end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date and end_date are required for custom period",
            )
        query = query.filter(
            models.Expense.created_at >= start_date,
            models.Expense.created_at <= end_date,
        )

    return query.order_by(models.Expense.created_at.desc()).all()


@router.get("/{expense_id}", response_model=expense_schemas.ExpenseOut)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.user_id == current_user.id,
        )
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=expense_schemas.ExpenseOut)
def update_expense(
    expense_id: int,
    expense_in: expense_schemas.ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.user_id == current_user.id,
        )
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    update_data = expense_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    expense = (
        db.query(models.Expense)
        .filter(
            models.Expense.id == expense_id,
            models.Expense.user_id == current_user.id,
        )
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
