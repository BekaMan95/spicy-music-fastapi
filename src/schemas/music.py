from pydantic import BaseModel, Json

class MusicBase(BaseModel):
    title: str
    artist: str
    album: str
    albumArt: str
    genre: Json
    email: str

class MusicCreate(MusicBase):
    password: str

class UserUpdate(MusicBase):
    albumArt: str | None

class MusicResponse(MusicBase):
    _id: int

    class Config:
        orm_mode = True
