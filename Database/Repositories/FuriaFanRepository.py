from Database.Entities.FuriaFanEntity import FuriaFanEntity  # Corrigido o caminho da entidade
from Database.Base.BaseRepository import BaseRepository  # Corrigido o caminho do repositório base

class FuriaFanRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, FuriaFanEntity)  # Passando a classe FuriaFanEntity para o repositório base

    def find_by_nome(self, nome: str):
        return self.db.query(self.model).filter(self.model.nome == nome).all()