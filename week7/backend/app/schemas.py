from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=5000)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class NotePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1, max_length=5000)


class ExtractionResult(BaseModel):
    action_items: list[str]
    tags: list[str]


class NotePage(BaseModel):
    items: list[NoteRead]
    total: int
    page: int
    page_size: int


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1, max_length=1000)


class ActionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class ActionItemPatch(BaseModel):
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    completed: bool | None = None


class ActionItemPage(BaseModel):
    items: list[ActionItemRead]
    total: int
    page: int
    page_size: int
