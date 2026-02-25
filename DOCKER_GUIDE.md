# Guía de Docker para ScooterFlow 🐳

### 1. Iniciar todo el sistema
Construye la imagen de la app y levanta la base de datos y la API juntas:
```powershell
docker-compose up --build
```
*   **API**: `http://localhost:8000`
*   **Swagger**: `http://localhost:8000/docs`

### 2. Iniciar solo la Base de Datos
Útil si quieres ejecutar la aplicación localmente con `uvicorn` pero necesitas la DB en Docker:
```powershell
docker-compose up -d db
```

### 3. Detener y Limpiar todo
Detiene los contenedores:
```powershell
docker-compose down
```
Detiene y **borra los datos** de la base de datos (limpieza total):
```powershell
docker-compose down -v
```

### 4. Ver logs
Si algo falla y quieres ver qué pasa en tiempo real:
```powershell
docker-compose logs -f
```
