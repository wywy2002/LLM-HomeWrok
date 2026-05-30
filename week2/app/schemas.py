from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    content: str = Field(min_length=1)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    created_at: str


class ActionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    note_id: int | None
    text: str
    done: bool
    created_at: str


class ActionItemExtractRequest(BaseModel):
    text: str = Field(min_length=1)
    save_note: bool = True


class ActionItemExtractResponse(BaseModel):
    note_id: int | None
    items: list[ActionItemRead]


class ActionItemDoneRequest(BaseModel):
    done: bool = True


class ActionItemDoneResponse(BaseModel):
    id: int
    done: bool


class LlmExtractRequest(BaseModel):
    text: str = Field(min_length=1)


class NotesListResponse(BaseModel):
    items: list[NoteRead]

