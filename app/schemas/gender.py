from pydantic import BaseModel

class GenderResponse(BaseModel):
    id: int
    name: str
    active: bool

    class Config:
        from_attributes = True