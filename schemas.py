# schemas.py

from pydantic import BaseModel

class FanBase(BaseModel):
    nome: str
    idade: int
    jogo_favorito: str
    localizacao: str

class FanCreate(FanBase):
    pass

class Fan(FanBase):
    id: int

    class Config:
        orm_mode = True

