from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from Database.Context.database import SessionLocal
from Database.Entities.FuriaFanEntity import FuriaFanEntity
from Schemas.FanSchemas import *

app = FastAPI(title="FURIA Fan Insights")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja os domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência para pegar o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para criar fã
@app.post("/fans/", response_model=Fan)
def criar_fan(fan: FanCreate, db: Session = Depends(get_db)):
    db_fan = FuriaFanEntity(**fan.dict())
    db.add(db_fan)
    db.commit()
    db.refresh(db_fan)
    return db_fan

# Função para filtrar fãs por jogo favorito
def filtrar_fas_por_jogo(fans_list, jogo_favorito):
    return [fan for fan in fans_list if fan['jogo_favorito'] == jogo_favorito]

# Função para filtrar fãs por localização
def filtrar_fas_por_localizacao(fans_list, localizacao):
    return [fan for fan in fans_list if fan['localizacao'] == localizacao]

# Rota para buscar fã por ID
@app.get("/fans/{fan_id}", response_model=Fan)
def obter_fan(fan_id: int, db: Session = Depends(get_db)):
    fan = db.query(FuriaFanEntity).filter(FuriaFanEntity.id == fan_id).first()
    if not fan:
        raise HTTPException(status_code=404, detail="Fã não encontrado")
    return fan

@app.put("/fans/{fan_id}", response_model=Fan)
def atualizar_fan(fan_id: int, fan: FanUpdate, db: Session = Depends(get_db)):
    db_fan = db.query(FuriaFanEntity).filter(FuriaFanEntity.id == fan_id).first()
    if not db_fan:
        raise HTTPException(status_code=404, detail="Fã não encontrado")

    for key, value in fan.dict().items():
        setattr(db_fan, key, value)  # Atualiza os campos do fã
    
    db.commit()
    db.refresh(db_fan)
    return db_fan

# Rota para filtrar fãs
@app.get("/fans/filter/")
def filtrar_fans(localizacao: str = None, jogo_favorito: str = None, db: Session = Depends(get_db)):
    query = db.query(models.FuriaFanEntity)
    
    if localizacao:
        query = query.filter(FuriaFanEntity.localizacao == localizacao)
    if jogo_favorito:
        query = query.filter(FuriaFanEntity.jogo_favorito == jogo_favorito)
    
    return query.all()

# Rota para listar todos os fãs
@app.get("/fans/", response_model=list[Fan])
def listar_fans(db: Session = Depends(get_db)):
    return db.query(FuriaFanEntity).all()

# Rota para deletar fã por ID
@app.delete("/fans/{fan_id}")
def deletar_fan(fan_id: int, db: Session = Depends(get_db)):
    fan = db.query(FuriaFanEntity).filter(FuriaFanEntity.id == fan_id).first()
    if not fan:
        raise HTTPException(status_code=404, detail="Fã não encontrado")

    db.delete(fan)
    db.commit()
    return {"mensagem": "Fã deletado com sucesso"}