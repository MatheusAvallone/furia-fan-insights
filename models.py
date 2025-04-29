# models.py

from sqlalchemy import Column, Integer, String
from database import Base

class FuriaFan(Base):
    __tablename__ = "furia_fans"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    jogo_favorito = Column(String)
    localizacao = Column(String)
