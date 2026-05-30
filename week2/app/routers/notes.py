from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import NoteCreate, NoteRead, NotesListResponse


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteRead)
def create_note(payload: NoteCreate) -> NoteRead:
    content = payload.content.strip()
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    return NoteRead.model_validate(dict(note))


@router.get("", response_model=NotesListResponse)
def get_all_notes() -> NotesListResponse:
    return NotesListResponse(items=[NoteRead.model_validate(row) for row in db.list_notes_dicts()])


@router.get("/{note_id}", response_model=NoteRead)
def get_single_note(note_id: int) -> NoteRead:
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteRead.model_validate(dict(row))


