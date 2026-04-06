from pydantic import BaseModel

class LevelResponse(BaseModel):
    id: int
    name: str
    active: bool

    class Config:
        from_attributes = True