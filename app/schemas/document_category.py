from pydantic import BaseModel

class DocumentCategoryResponse(BaseModel):
    id: int
    name: str
    active: bool

    class Config:
        from_attributes = True