#el archivo main doned se ejcuta todo lo perteneciente a /app

#los imports
import logging
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import authors, books, members, library_books, loans
from app import models


#Logging básico
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger("app")

app = FastAPI(title="Library API", version="0.2.0")

@app.on_event("startup")
def on_startup():
    #creo las tablas si no exiten
    Base.metadata.create_all(bind=engine)
    logger.info("DB tables ensured and app started")

@app.get("/health", tags=["meta"])
def health():
    #compruebo de vida del servicio
    return {"status": "ok"}
#registro cada grupo de rutas
#Dejo el resto activas pero la elegida para la evaluacion es books
app.include_router(authors.router)
app.include_router(books.router) # ENTIDAD PRINCIPAL
app.include_router(members.router)
app.include_router(library_books.router)
app.include_router(loans.router)