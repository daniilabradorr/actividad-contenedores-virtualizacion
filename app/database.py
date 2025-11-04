#Los imports
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

logger = logging.getLogger(__name__)

#la url la dejo muy similar al profesor ya que me gusto su modularizacion de los archivos
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./dev.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
#creo el engine de la BBDD
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


#Inicio la sesion con la configuracion de los commits y que no empuje los cambios a la db ates de cada consulta
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

#la clase declarativa
class Base(DeclarativeBase):
    pass

#creo una sesion por peticion y la cierro automarticamnet al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()