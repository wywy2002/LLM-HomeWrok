from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import (
    ActionItemBulkComplete,
    ActionItemCreate,
    ActionItemPatch,
    ActionItemRead,
    ActionItemsPage,
)

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=list[ActionItemRead])
def list_items(
    db: Session = Depends(get_db), completed: Optional[bool] = None
) -> list[ActionItemRead]:
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))
    rows = db.execute(stmt).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.get("/page", response_model=ActionItemsPage)
def list_items_page(
    db: Session = Depends(get_db),
    completed: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort: str = Query("created_desc"),
) -> ActionItemsPage:
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    sort_map = {"created_desc": desc(ActionItem.id), "description_asc": asc(ActionItem.description)}
    rows = db.execute(
        stmt.order_by(sort_map.get(sort, desc(ActionItem.id))).offset((page - 1) * page_size).limit(page_size)
    ).scalars().all()
    return ActionItemsPage(
        items=[ActionItemRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.patch("/{item_id}", response_model=ActionItemRead)
def patch_item(item_id: int, payload: ActionItemPatch, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    if payload.description is not None:
        item.description = payload.description
    if payload.completed is not None:
        item.completed = payload.completed
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.post("/bulk-complete", response_model=list[ActionItemRead])
def bulk_complete(payload: ActionItemBulkComplete, db: Session = Depends(get_db)) -> list[ActionItemRead]:
    items: list[ActionItem] = []
    for item_id in payload.ids:
        item = db.get(ActionItem, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"Action item {item_id} not found")
        item.completed = True
        db.add(item)
        items.append(item)
    db.flush()
    for item in items:
        db.refresh(item)
    return [ActionItemRead.model_validate(item) for item in items]
