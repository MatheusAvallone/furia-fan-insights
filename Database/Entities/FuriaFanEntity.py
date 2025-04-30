from sqlalchemy import Column, Integer, String
from Database.Context.database import Base

class FuriaFanEntity(Base):
    __tablename__ = "furia_fans"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    jogo_favorito = Column(String)
    localizacao = Column(String)