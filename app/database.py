import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

logger = logging.getLogger(__name__)

#Lee la URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db").strip()


is_sqlite = DATABASE_URL.startswith("sqlite")

engine_kwargs = {"pool_pre_ping": True}  # opcional: evita conexiones muertas
if is_sqlite:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

#Creo el engine
engine = create_engine(DATABASE_URL, **engine_kwargs)

#Sesion
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

#Base declarativa
class Base(DeclarativeBase):
    pass

#Dependencia de DB por petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()