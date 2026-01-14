from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class StatusSchema(BaseModel):
    code: int
    message: str


class ApiResponse(BaseModel, Generic[T]):
    status: StatusSchema
    data: Optional[T] = None
