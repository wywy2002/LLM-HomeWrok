from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session, selectinload

from ..db import get_db
from ..models import Note, Tag
from ..schemas import (
    ExtractionResult,
    NoteCreate,
    NotePage,
    NotePatch,
    NoteRead,
    NoteTagAttach,
    TagCreate,
    TagRead,
)
from ..services.extract import extract_action_items, extract_tags

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    stmt = select(Note).options(selectinload(Note.tags))
    if q:
        q_like = f"%{q.lower()}%"
        stmt = stmt.where(func.lower(Note.title).like(q_like) | func.lower(Note.content).like(q_like))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Note, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Note, sort_field)))
    else:
        stmt = stmt.order_by(desc(Note.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NotePatch, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.put("/{note_id}", response_model=NoteRead)
def replace_note(note_id: int, payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = payload.title
    note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> None:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()


@router.get("/search/page", response_model=NotePage)
def search_notes_page(
    q: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort: str = Query("created_desc"),
    db: Session = Depends(get_db),
) -> NotePage:
    stmt = select(Note).options(selectinload(Note.tags))
    if q:
        q_like = f"%{q.lower()}%"
        stmt = stmt.where(func.lower(Note.title).like(q_like) | func.lower(Note.content).like(q_like))

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    sort_map = {
        "created_desc": desc(Note.created_at),
        "title_asc": asc(Note.title),
    }
    stmt = stmt.order_by(sort_map.get(sort, desc(Note.created_at)))
    offset = (page - 1) * page_size
    rows = db.execute(stmt.offset(offset).limit(page_size)).scalars().all()
    return NotePage(
        items=[NoteRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.execute(select(Note).options(selectinload(Note.tags)).where(Note.id == note_id)).scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.get("/tags/all", response_model=list[TagRead], tags=["tags"])
def list_tags(db: Session = Depends(get_db)) -> list[TagRead]:
    rows = db.execute(select(Tag).order_by(Tag.name.asc())).scalars().all()
    return [TagRead.model_validate(row) for row in rows]


@router.post("/tags/all", response_model=TagRead, status_code=201, tags=["tags"])
def create_tag(payload: TagCreate, db: Session = Depends(get_db)) -> TagRead:
    existing = db.execute(select(Tag).where(func.lower(Tag.name) == payload.name.lower())).scalar_one_or_none()
    if existing:
        return TagRead.model_validate(existing)
    tag = Tag(name=payload.name.lower())
    db.add(tag)
    db.flush()
    db.refresh(tag)
    return TagRead.model_validate(tag)


@router.delete("/tags/{tag_id}", status_code=204, tags=["tags"])
def delete_tag(tag_id: int, db: Session = Depends(get_db)) -> None:
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.flush()


@router.post("/{note_id}/tags", response_model=NoteRead)
def attach_tag(note_id: int, payload: NoteTagAttach, db: Session = Depends(get_db)) -> NoteRead:
    note = db.execute(select(Note).options(selectinload(Note.tags)).where(Note.id == note_id)).scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    tag = db.get(Tag, payload.tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    if all(existing.id != tag.id for existing in note.tags):
        note.tags.append(tag)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.delete("/{note_id}/tags/{tag_id}", response_model=NoteRead)
def detach_tag(note_id: int, tag_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.execute(select(Note).options(selectinload(Note.tags)).where(Note.id == note_id)).scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.tags = [tag for tag in note.tags if tag.id != tag_id]
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.post("/{note_id}/extract", response_model=ExtractionResult)
def extract_note(note_id: int, apply: bool = False, db: Session = Depends(get_db)) -> ExtractionResult:
    note = db.execute(select(Note).options(selectinload(Note.tags)).where(Note.id == note_id)).scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    action_items = extract_action_items(note.content)
    tags = extract_tags(note.content)
    if apply:
        for tag_name in tags:
            tag = db.execute(select(Tag).where(Tag.name == tag_name)).scalar_one_or_none()
            if tag is None:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()
            if all(existing.id != tag.id for existing in note.tags):
                note.tags.append(tag)
        db.add(note)
        db.flush()
    return ExtractionResult(action_items=action_items, tags=tags)


