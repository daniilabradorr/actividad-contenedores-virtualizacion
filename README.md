# 📚 Library API (FastAPI) — Actividad de Contenedores & Virtualización

Reutilizo el ejercicio de programación avanzada (**FastAPI** + **SQLAlchemy** + **Pydantic**) y lo adaptamo a la actividad de Contenedores y Virtualización.

Para la evaluación del enunciado he elegido como entidad principal: **books (CRUD completo)**.

> **Nota:** He dejado activos el resto de *routers* (authors, members, library\_books, loans) por si usted profesor desea explorar más casos. **No son necesarios para superar la actividad**, pero lo que hecho porque se que amplían el ejercicio.

-----

## ✅ Cumplimiento de la actividad

| Requisito | Cumplimiento |
| :--- | :--- |
| **API HTTP en puerto 8080** accesible desde el host | El servicio `biblioteca-api` expone **8080:8080**. |
| **CRUD mínimo** (usamos `books`) | `GET /books` (listar), `GET /books/{id}` (detalle), `POST /books` (crear), `DELETE /books/{id}` (borrar). |
| **Control de errores y validación** | **404** (no encontrado), **409** (conflictos como ISBN duplicado), **422/400** (validación de Pydantic). |
| **Logging mínimo** | Configurado en `app/main.py` con `logging.basicConfig(level=INFO)`. |
| **Persistencia en BD** | **PostgreSQL** en contenedor con **volumen nombrado** `biblioteca-postgres-data`. |
| **Red propia** | Ambos contenedores conviven en la red **`biblioteca-net`** y se comunican por nombre de servicio (`biblioteca-db`). |
| **Imagen construida con compose** | `docker-compose up --build`. |

-----

## 🧩 Estructura del Proyecto

```
app/
  main.py
  database.py
  models.py
  schemas.py
  routers/
    authors.py
    books.py        # ENTIDAD EVALUADA (CRUD mínimo)
    members.py
    library_books.py
    loans.py
scripts/
  seed.py           # script (poblar datos de ejemplo)
Dockerfile
docker-compose.yml
.env.example        # pense que sería buena idea que viese como hago un .env
requirements.txt
README.md
```

-----

## 🔐 Variables de Entorno

Creo el archivo **`.env.example`** (ejemplo del .env):

```
POSTGRES_USER=biblioteca_user
POSTGRES_PASSWORD=biblioteca_pass
POSTGRES_DB=biblioteca_db
DATABASE_URL=postgresql+psycopg2://biblioteca_user:biblioteca_pass@biblioteca-db:5432/biblioteca_db
```

> **Importante:** `DATABASE_URL` uso **`biblioteca-db`** (nombre del contenedor de la BD) como host para la comunicación dentro de la red Docker.

-----

## 🐳 Docker Compose (`docker-compose.yml`)

A continuación, te describo un resumen del contenido relevante para la configuración de la BD, la API, el volumen y la red con nombre(aunque sea una actividad esto es un README):

```yaml
version: "3.9"
services:
  biblioteca-db:
    image: postgres:16
    container_name: biblioteca-db
    restart: always
    env_file:
      - .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - biblioteca-postgres-data:/var/lib/postgresql/data # Volumen nombrado para persistencia
    networks:
      - biblioteca-net # Red propia

  biblioteca-api:
    build: .
    container_name: biblioteca-api
    ports:
      - "8080:8080"
    depends_on:
      - biblioteca-db
    env_file:
      - .env
    environment:
      DATABASE_URL: ${DATABASE_URL}
    networks:
      - biblioteca-net # Red propia

volumes:
  biblioteca-postgres-data:
    name: biblioteca-postgres-data   # Volumen con nombre explícito

networks:
  biblioteca-net:
    name: biblioteca-net             # Red con nombre explícito
```

-----

## 🛠️ Dockerfile (Imagen de la API)

```dockerfile
FROM python:3.11-slim
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

-----

## 🚀 Puesta en Marcha

```bash
# Construir y arrancar ambos servicios (BD y API)
docker-compose up --build
```

### Documentación Interactiva (Swagger/OpenAPI)

Accede a: [http://localhost:8080/docs](https://www.google.com/search?q=http://localhost:8080/docs)

> En el arranque, la app crea las tablas si no existen (`Base.metadata.create_all(bind=engine)`).

-----

## 🧪 CRUD Evaluado: `books` (Endpoints Mínimos)

  * `GET /books` → `200`, lista de libros (filtros opcionales).
  * `GET /books/{id}` → `200` ó `404` si no existe.
  * `POST /books` → `201`; valida isbn único y `author_id` existente; `409` si hay conflicto.
  * `DELETE /books/{id}` → `204` si borra; `404` si no existe.

### cURL de Prueba Rápida

```bash
# 1) Crear autor (para tener author_id válido)
curl -X POST http://localhost:8080/authors \
  -H "Content-Type: application/json" \
  -d '{"name":"Isaac Asimov"}'

# 2) Crear libro (sustituye author_id por el devuelto arriba)
curl -X POST http://localhost:8080/books \
  -H "Content-Type: application/json" \
  -d '{"isbn":"978000000001","title":"Fundación","category":"SciFi","author_id":1}'

# 3) Listar libros
curl http://localhost:8080/books

# 4) Consultar libro por ID
curl http://localhost:8080/books/1

# 5) Borrar libro
curl -X DELETE http://localhost:8080/books/1
```

### Alternativa: Poblar Datos de Ejemplo(que use para ver si funcionaba)

```bash
docker-compose exec biblioteca-api python scripts/seed.py
```

-----

## 🪵 Logging (Trazabilidad Mínima que pedia la actividad)

Configurado en `app/main.py`:

```python
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
```

**Ejemplos de logs en `books.py` (creación de libro):**

  * `INFO` al crear libro (ISBN, título).
  * `WARNING` si `author_id` no existe o si `isbn` está duplicado.

-----

## 🔎 Routers Extra Activos

*(para que usted profesor pruebe mas casos si quiere)*

Orden lógico recomendado:

1.  **`authors`** → crear autor.
2.  **`books`** → crear libro con `author_id`.
3.  **`members`** → crear socio.
4.  **`library_books`** → crear ejemplar físico de un libro.
5.  **`loans`** → prestar / devolver / marcar tarde.

> **Importante:** Para la actividad **solo evaluamos `books`**; los demás *routers* quedan activos para ampliar y facilitar pruebas.

-----

## 🧱 Verificación de Persistencia y Red

### Volumen con Nombre

```bash
docker volume ls | grep biblioteca-postgres-data
```

### Red con Nombre

```bash
docker network ls | grep biblioteca-net
```

### Persistencia (Crear datos, parar y volver a subir)

```bash
docker-compose down
docker-compose up
```

-----

## 🧪 Comprobaciones Rápidas (Checklist)

  * [ ] `docker-compose up --build` arranca sin errores.
  * [ ] `http://localhost:8080/health` devuelve `{"status":"ok"}`.
  * [ ] `POST /books` → `201` con `author_id` válido; `409` en ISBN duplicado.
  * [ ] Datos persisten tras `down` y `up` (volumen `biblioteca-postgres-data`).
  * [ ] Red `biblioteca-net` creada y servicios comunicándose por nombre.
  * [ ] Logging visible en consola (`INFO`).

-----

## 📦 Notas Técnicas

  * `requirements.txt` incluye `psycopg2-binary` para PostgreSQL.
  * `app/database.py` lee `DATABASE_URL` desde entorno.
  * `.env` **no se versiona**; `.env.example` **sí**.
  * `.dockerignore` evita incluir `.env` y ficheros innecesarios en la imagen.
  * En producción se usarían migraciones (Alembic); para la actividad, `create_all` es suficiente.

-----

## 📝 Autoría

Ejercicio académico, adaptado para la actividad de Contenedores y Virtualización.

**Autoría:** daniilabradorr (Daniel Labrador Benito).

-----