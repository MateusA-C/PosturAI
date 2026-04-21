from sqlalchemy import create_engine,Column,String,Integer,Boolean,ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base
from datetime import datetime

db = create_engine("sqlite:///posturai.db",connect_args={"check_same_thread": False})
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    idade = Column("idade",Integer)
    nome = Column("nome", String)
    email = Column("email", String)
    senha = Column("senha", String)
    profissao = Column("profissao", String)
    sexo = Column("sexo",String)

    def __init__(self, nome, email, senha, profissao,idade,sexo):
        self.nome = nome
        self.idade = idade # E aqui
        self.email = email
        self.senha = senha
        self.profissao = profissao
        self.sexo = sexo

class Registro(Base):
    __tablename__ = "registros"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    data = Column("data",String)
    QAF = Column("QAF", Integer,default=0)
    QAT = Column("QAT", Integer,default=0)
    usuario_id = Column("usuario_id", ForeignKey("usuarios.id"))

    def __init__(self,usuario_id):
        
        self.usuario_id = usuario_id
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.QAF = 0
        self.QAT = 0

Base.metadata.create_all(bind=db)