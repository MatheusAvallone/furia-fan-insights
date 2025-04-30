from pydantic import BaseModel

# Schema de entrada (POST)
class FanCreate(BaseModel):
    nome: str
    idade: int
    jogo_favorito: str
    localizacao: str

# Schema de saída (GET/POST)
class Fan(FanCreate):
    id: int

    class Config:
        from_attributes = True

class FanUpdate(BaseModel):
    nome: str
    idade: int
    jogo_favorito: str
    localizacao: str