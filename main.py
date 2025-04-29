# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from twitter_api import buscar_tweets

# Cria as tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FURIA Fan Insights")

# Permitir frontend e chamadas externas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja os origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função de dependência de sessão com o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para filtrar fãs por jogo favorito
def filtrar_fas_por_jogo(fans_list, jogo_favorito):
    return [fan for fan in fans_list if fan['jogo_favorito'] == jogo_favorito]

# Função para filtrar fãs por localização
def filtrar_fas_por_localizacao(fans_list, localizacao):
    return [fan for fan in fans_list if fan['localizacao'] == localizacao]

# Rota para criar um novo fã
@app.post("/fans/", response_model=schemas.Fan)
def criar_fan(fan: schemas.FanCreate, db: Session = Depends(get_db)):
    db_fan = models.FuriaFan(**fan.dict())
    db.add(db_fan)
    db.commit()
    db.refresh(db_fan)
    return db_fan

# Rota para buscar fã por ID
@app.get("/fans/{fan_id}", response_model=schemas.Fan)
def obter_fan(fan_id: int, db: Session = Depends(get_db)):
    fan = db.query(models.FuriaFan).filter(models.FuriaFan.id == fan_id).first()
    if not fan:
        raise HTTPException(status_code=404, detail="Fã não encontrado")
    return fan

@app.put("/fans/{fan_id}", response_model=schemas.Fan)
def atualizar_fan(fan_id: int, fan: schemas.FanCreate, db: Session = Depends(get_db)):
    db_fan = db.query(models.FuriaFan).filter(models.FuriaFan.id == fan_id).first()
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
    query = db.query(models.FuriaFan)
    
    if localizacao:
        query = query.filter(models.FuriaFan.localizacao == localizacao)
    if jogo_favorito:
        query = query.filter(models.FuriaFan.jogo_favorito == jogo_favorito)
    
    return query.all()

# Função para buscar tweets relacionados
@app.get("/tweets/{fan_id}")
def get_tweets_por_fan(fan_id: int, db: Session = Depends(get_db)):
    fan = db.query(models.FuriaFan).filter(models.FuriaFan.id == fan_id).first()
    if not fan:
        raise HTTPException(status_code=404, detail="Fã não encontrado")
    
    tweets = buscar_tweets(sobre_o_que=fan.nome)
    return tweets

# Rota para listar todos os fãs
@app.get("/fans/", response_model=list[schemas.Fan])
def listar_fans(db: Session = Depends(get_db)):
    return db.query(models.FuriaFan).all()

# Rota para deletar fã por ID
@app.delete("/fans/{fan_id}")
def deletar_fan(fan_id: int, db: Session = Depends(get_db)):
    fan = db.query(models.FuriaFan).filter(models.FuriaFan.id == fan_id).first()
    if not fan:
        raise HTTPException(status_code=404, detail="Fã não encontrado")

    db.delete(fan)
    db.commit()
    return {"mensagem": "Fã deletado com sucesso"}





