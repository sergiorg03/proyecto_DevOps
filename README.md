# 🛴 ScooterFlow API

API REST para la gestión de una flota de patinetes eléctricos urbanos. Desarrollada con **FastAPI**, **PostgreSQL** y desplegada con **Docker**.

---

## 🧱 Arquitectura del Proyecto

```
proyecto_DevOps/
├── app/
│   ├── main.py          # Endpoints de la API (FastAPI)
│   ├── crud.py          # Lógica de negocio y acceso a datos
│   ├── models.py        # Modelos SQLAlchemy (tablas de la BD)
│   ├── schemas.py       # Modelos Pydantic (validación de datos)
│   ├── database.py      # Configuración de conexión a PostgreSQL
│   └── deps.py          # Dependencia de sesión de base de datos
├── migrations/          # Migraciones de Alembic
│   └── versions/        # Historial de cambios del esquema
├── tests/
│   ├── conftest.py      # Fixtures de pytest (BD en memoria)
│   └── test_main.py     # Tests de la API (22 tests)
├── .github/
│   └── workflows/
│       └── ci.yaml      # Pipeline CI/CD con GitHub Actions
├── Dockerfile           # Imagen de la aplicación
├── docker-compose.yaml  # Orquestación de servicios
├── requirements.txt     # Dependencias de Python
└── .env                 # Variables de entorno (local)
```

---

## 🚀 Levantar el Proyecto (con Docker)

### Prerrequisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.

### Paso 1: Clonar el repositorio

```bash
git clone <https://github.com/sergiorg03/proyecto_DevOps.git>
cd proyecto_DevOps
```

### Paso 2: Levantar todos los servicios con un solo comando

```bash
docker-compose up --build -d
```

Este comando realiza automáticamente lo siguiente:
1. **Construye** la imagen Docker de la aplicación FastAPI.
2. **Levanta** el contenedor de **PostgreSQL** (`scooterflow_db`).
3. **Espera** a que la base de datos esté lista (healthcheck).
4. **Levanta** el contenedor de la **API** (`scooterflow_app`) una vez la BD está sana.

> **Nota:** En el primer arranque la base de datos estará vacía. Ejecuta las migraciones (ver paso 3).

### Paso 3: Aplicar las migraciones de Alembic

En una terminal aparte, con los contenedores activos:

```bash
docker-compose exec app alembic upgrade head
```

Esto crea las tablas `zone` y `scooter` en la base de datos PostgreSQL.

### Paso 4: (Opcional) Poblar la base de datos con datos iniciales

```bash
docker-compose exec app python seed.py
```

---

## 🌐 Acceder a la API

| Recurso | URL |
|---|---|
| **API Base** | `http://localhost:8000` |
| **Documentación Swagger** | `http://localhost:8000/docs` |

---

## 📡 Endpoints Disponibles

### Zonas (`/zones/`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/zones/` | Listar todas las zonas |
| `GET` | `/zones/{id}` | Obtener una zona por ID |
| `POST` | `/zones/` | Crear una nueva zona |
| `DELETE` | `/zones/{id}` | Eliminar una zona (borra sus patinetes en cascada) |
| `POST` | `/zones/{id}/mantenimiento` | Poner en mantenimiento patinetes con batería < 15% |

### Patinetes (`/scooters/`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/scooters/` | Listar todos los patinetes |
| `GET` | `/scooters/{id}` | Obtener un patinete por ID |
| `POST` | `/scooters/` | Crear un nuevo patinete |
| `DELETE` | `/scooters/{id}` | Eliminar un patinete |

---

## 🧪 Ejecutar los Tests

Los tests utilizan una base de datos SQLite en memoria, por lo que **no requieren Docker**.

```bash
# Activar el entorno virtual
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# Ejecutar todos los tests
pytest tests/test_main.py

# Ejecutar con detalle
pytest tests/test_main.py -v
```

La suite cubre **22 tests** entre casos positivos y negativos:
- CRUD de zonas y patinetes
- Borrado en cascada
- Validaciones (batería, estado, campos obligatorios)
- Lógica de mantenimiento automático

---

## 🤖 CI/CD con GitHub Actions

El pipeline se activa automáticamente en cada `push` o `pull_request` a la rama `main`:

1. Levanta un servicio de **PostgreSQL 15** en el runner.
2. Instala las dependencias de Python.
3. Espera a que la base de datos esté disponible.
4. Ejecuta `alembic upgrade head` para crear las tablas.
5. Lanza `pytest` para validar la suite de tests.

---

## 🐳 Comandos Docker Útiles

```bash
# Levantar en segundo plano (modo detached)
docker-compose up --build -d

# Ver logs en tiempo real
docker-compose logs -f

# Detener los contenedores
docker-compose down

# Detener y borrar los datos de la BD (limpieza total)
docker-compose down -v

# Levantar solo la base de datos (para desarrollo local)
docker-compose up -d db
```

---

## ⚗️ Gestión de Migraciones (Alembic)

```bash
# Generar una nueva migración tras modificar models.py
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar todas las migraciones pendientes
alembic upgrade head

# Revertir la última migración
alembic downgrade -1

# Ver el historial de migraciones
alembic history --verbose
```
