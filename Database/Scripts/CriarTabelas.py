import sys
from pathlib import Path

# Adicionando o diretório raiz ao sys.path
root_dir = str(Path(__file__).parent.parent.parent)  # Isso leva até a raiz (furia-fan-insights)
sys.path.append(root_dir)

from Database.Context.database import engine, Base
from Database.Entities.FuriaFanEntity import FuriaFanEntity  # IMPORTANTE!

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso.")