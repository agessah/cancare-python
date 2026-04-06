from pydantic import BaseModel

class MediaTypeResponse(BaseModel):
    id: int
    name: str
    active: bool

    class Config:
        from_attributes = True