#el archivo main doned se ejcuta todo lo perteneciente a /app

#los imports
from fastapi import FastAPI
from app.routers import authors, books, members, library_books, loans

app = FastAPI(title="Library API", version="0.2.0")

@app.get("/health", tags=["meta"])
def health():
    #uso esto para ver que el servicio está vivo
    return {"status": "ok"}

#registro cada grupo de rutas
#Dejo el resto activas pero la elegida para la evaluacion es books
app.include_router(authors.router)
app.include_router(books.router) # ENTIDAD PRINCIPAL
app.include_router(members.router)
app.include_router(library_books.router)
app.include_router(loans.router)