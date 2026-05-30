from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=5000)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str


class NotePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1, max_length=5000)


class NotesPage(BaseModel):
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


class ActionItemPatch(BaseModel):
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    completed: bool | None = None


class ActionItemBulkComplete(BaseModel):
    ids: list[int] = Field(min_length=1)


class ActionItemsPage(BaseModel):
    items: list[ActionItemRead]
    total: int
    page: int
    page_size: int
