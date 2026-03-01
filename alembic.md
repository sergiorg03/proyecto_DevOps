# ⚗️ Guía de Alembic: Gestión de Migraciones

Alembic es una herramienta de migración de bases de datos para **SQLAlchemy**. Permite gestionar la evolución del esquema de tu base de datos de la misma forma que gestionas tu código: mediante un historial de versiones.

---

## 🤔 ¿Qué es Alembic?

En el desarrollo de aplicaciones, los modelos de datos cambian constantemente (añadir columnas, crear tablas, etc.). En lugar de borrar la base de datos y recrearla, o ejecutar comandos SQL manuales, Alembic:
1.  **Detecta cambios**: Compara tus modelos de Python con el estado actual de la base de datos.
2.  **Genera scripts**: Crea archivos de migración automáticos.
3.  **Mantiene el historial**: Permite subir de versión o volver atrás (rollback) de forma segura.

---

## 🛠️ Comandos Más Importantes

Aquí tienes los comandos fundamentales que usarás en el día a día:

### 1. Inicialización
```bash
alembic init migrations
```
Crea la estructura necesaria en tu proyecto (la carpeta `migrations` y el archivo `alembic.ini`). Solo se ejecuta **una vez** al principio del proyecto.

### 2. Crear una Migración (Revisión)
```bash
alembic revision --autogenerate -m "Descripción del cambio"
```
-   `--autogenerate`: Compara tus modelos en `models.py` con la base de datos y escribe el código de la migración por ti.
-   `-m`: Añade un comentario descriptivo al archivo generado.

### 3. Aplicar Cambios (Upgrade)
```bash
alembic upgrade head
```
Aplica todas las migraciones pendientes hasta llegar a la versión más reciente (`head`). Este es el comando que "crea" o "modifica" las tablas reales en tu DB.

### 4. Deshacer Cambios (Downgrade)
```bash
alembic downgrade -1
```
Revierte la última migración aplicada. Útil si has cometido un error en el último cambio del esquema.

### 5. Ver el Historial
```bash
alembic history --verbose
```
Muestra una lista de todas las migraciones creadas, su identificador único y si han sido aplicadas o no.

---

## 💡 Flujo de Trabajo Recomendado

1.  **Modifica** tus clases en `app/models.py`.
2.  **Genera** la migración: `alembic revision --autogenerate -m "añadir columna X"`.
3.  **Revisa** el archivo generado en `migrations/versions/`.
4.  **Aplica** el cambio: `alembic upgrade head`.

---
> [!TIP]
> **Importante**: Nunca borres manualmente la tabla `alembic_version` de tu base de datos, ya que es donde Alembic guarda en qué punto del historial se encuentra tu sistema.
