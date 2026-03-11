from pydantic import BaseModel


class SessionData(BaseModel):
    session_id: int
    state: str


class SessionResponse(BaseModel):
    status: str
    data: SessionData
