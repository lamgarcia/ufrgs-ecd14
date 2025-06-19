from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Session
from enum import Enum
import os

app = FastAPI(
    title="Serviço de Agenda",
    description="Gerencia contatos com números de telefone.",
)

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Enums
class TipoTelefone(str, Enum):
    movel = "movel"
    fixo = "fixo"
    comercial = "comercial"

class CategoriaContato(str, Enum):
    pessoal = "pessoal"
    familiar = "familiar"
    comercial = "comercial"

# Modelos SQLAlchemy
class ContatoDB(Base):
    __tablename__ = "contatos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(SqlEnum(CategoriaContato), nullable=False)

    telefones = relationship("TelefoneDB", back_populates="contato", cascade="all, delete-orphan")

class TelefoneDB(Base):
    __tablename__ = "telefones"
    id = Column(Integer, primary_key=True)
    numero = Column(String, nullable=False)
    tipo = Column(SqlEnum(TipoTelefone), nullable=False)
    contato_id = Column(Integer, ForeignKey("contatos.id"))

    contato = relationship("ContatoDB", back_populates="telefones")

# Pydantic Schemas
class Telefone(BaseModel):
    numero: str
    tipo: TipoTelefone

class ContatoBase(BaseModel):
    nome: str
    categoria: CategoriaContato
    telefones: list[Telefone]

class ContatoCreate(ContatoBase):
    pass

class Contato(ContatoBase):
    id: int
    class Config:
        from_attributes = True

# Criação de tabelas
def create_db_tables():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    create_db_tables()

# Dependência do DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas
@app.post("/contato", response_model=Contato, status_code=201)
def criar_contato(contato: ContatoCreate, db: Session = Depends(get_db)):
    novo_contato = ContatoDB(nome=contato.nome, categoria=contato.categoria)
    db.add(novo_contato)
    db.commit()
    db.refresh(novo_contato)

    for tel in contato.telefones:
        db_tel = TelefoneDB(numero=tel.numero, tipo=tel.tipo, contato_id=novo_contato.id)
        db.add(db_tel)

    db.commit()
    db.refresh(novo_contato)
    return novo_contato

@app.get("/contatos", response_model=list[Contato])
def listar_contatos(db: Session = Depends(get_db)):
    return db.query(ContatoDB).all()

@app.get("/contato/{contato_id}", response_model=Contato)
def consultar_contato(contato_id: int, db: Session = Depends(get_db)):
    contato = db.query(ContatoDB).filter(ContatoDB.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return contato

@app.delete("/contato/{contato_id}", response_model=dict)
def deletar_contato(contato_id: int, db: Session = Depends(get_db)):
    contato = db.query(ContatoDB).filter(ContatoDB.id == contato_id).first()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    
    db.delete(contato)
    db.commit()
    return {"message": "Contato apagado com sucesso", "success": True}
