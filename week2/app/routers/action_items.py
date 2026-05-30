from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import (
    ActionItemDoneRequest,
    ActionItemDoneResponse,
    ActionItemExtractRequest,
    ActionItemExtractResponse,
    ActionItemRead,
)
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ActionItemExtractResponse)
def extract(payload: ActionItemExtractRequest) -> ActionItemExtractResponse:
    text = payload.text.strip()
    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items(text)
    ids = db.insert_action_items(items, note_id=note_id)
    rows = [db.get_action_item(item_id) for item_id in ids]
    return ActionItemExtractResponse(
        note_id=note_id,
        items=[ActionItemRead.model_validate(dict(row)) for row in rows if row is not None],
    )


@router.post("/extract-llm", response_model=list[str])
def extract_with_llm(payload: ActionItemExtractRequest) -> list[str]:
    return extract_action_items_llm(payload.text)


@router.get("", response_model=list[ActionItemRead])
def list_all(note_id: Optional[int] = None) -> list[ActionItemRead]:
    rows = db.list_action_items(note_id=note_id)
    return [ActionItemRead.model_validate(dict(r) | {"done": bool(r["done"])}) for r in rows]


@router.post("/{action_item_id}/done", response_model=ActionItemDoneResponse)
def mark_done(action_item_id: int, payload: ActionItemDoneRequest) -> ActionItemDoneResponse:
    try:
        db.mark_action_item_done(action_item_id, payload.done)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ActionItemDoneResponse(id=action_item_id, done=payload.done)


