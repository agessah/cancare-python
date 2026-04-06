from pydantic import BaseModel

class FollowUpStatusResponse(BaseModel):
    id: int
    name: str
    active: bool

    class Config:
        from_attributes = True