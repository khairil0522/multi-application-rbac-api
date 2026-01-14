from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    code: str
    name: str

class ApplicationUpdate(BaseModel):
    name: str | None = None

class ApplicationResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool

    class Config:
        from_attributes = True
