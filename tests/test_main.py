from fastapi.testclient import TestClient

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "API funcionando"}

'''
    TEST ZONAS
'''

def test_get_zones(client: TestClient):
    response = client.get("/zones/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_zonas_id_corr(client: TestClient):
    response = client.get("/zones/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_zonas_id_incorr(client: TestClient):
    response = client.get("/zones/-100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Zona no encontrada"}

def test_create_zone(client: TestClient):
    new_zone = {"nombre": "Test Zone", "codigo_postal": 28000, "limite_velocidad": 25}
    response = client.post("/zones/", json=new_zone)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Test Zone"
    assert "id" in data

def test_delete_zone(client: TestClient):
    # Deleting the seeded zone (id=1)
    response = client.delete("/zones/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Zona eliminada"}
    
    # Verify it's gone
    get_resp = client.get("/zones/1")
    assert get_resp.status_code == 404

    # Verify it's gone
    get_resp = client.get("/zones/1")
    assert get_resp.status_code == 404

def test_delete_zone_cascade(client: TestClient):
    # Verificación de existencia del scooter con ID=1
    check_scooter = client.get("/scooters/1")
    assert check_scooter.status_code == 200

    # Eliminamos la zona con ID=1
    client.delete("/zones/1")
    
    # Vericación de existencia en la BD
    check_scooter_deleted = client.get("/scooters/1")
    assert check_scooter_deleted.status_code == 404

def test_create_zone_invalid_speed(client: TestClient):
    new_zone = {"nombre": "Speedy", "codigo_postal": 28000, "limite_velocidad": -10}
    response = client.post("/zones/", json=new_zone)
    assert response.status_code == 400
    assert response.json()["detail"] == "El límite de velocidad no puede ser negativo"

def test_create_scooter_invalid_battery(client: TestClient):
    new_scooter = {
        "numero_serie": "BATT-ERR",
        "modelo": "Test",
        "bateria": 150,
        "estado": "disponible",
        "zona_id": 1
    }
    response = client.post("/scooters/", json=new_scooter)
    assert response.status_code == 422
    assert "batería debe estar entre 0 y 100" in response.json()["detail"][0]["msg"]

def test_create_scooter_non_existent_zone(client: TestClient):
    new_scooter = {
        "numero_serie": "ZONE-ERR",
        "modelo": "Test",
        "bateria": 50,
        "estado": "disponible",
        "zona_id": 999
    }
    response = client.post("/scooters/", json=new_scooter)
    assert response.status_code == 404
    assert response.json()["detail"] == "Zona no encontrada"

'''
    TEST SCOOTERS
'''

def test_get_scooters_corr(client: TestClient):
    response = client.get("/scooters/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_scooter_id_corr(client: TestClient):
    response = client.get("/scooters/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_scooter_id_incorr(client: TestClient):
    response = client.get("/scooters/-100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Patinete no encontrado"}

def test_create_scooter(client: TestClient):
    new_scooter = {
        "numero_serie": "TEST-001",
        "modelo": "Test Model",
        "bateria": 90,
        "estado": "disponible",
        "zona_id": 1
    }
    response = client.post("/scooters/", json=new_scooter)
    assert response.status_code == 200
    data = response.json()
    assert data["numero_serie"] == "TEST-001"

def test_delete_scooter(client: TestClient):
    # Eliminado el scooter con ID=1 añadido para los tests
    response = client.delete("/scooters/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Patinete eliminado"}
    
    # Vericación de existencia en la BD
    get_resp = client.get("/scooters/1")
    assert get_resp.status_code == 404

def test_create_scooter_incorr(client: TestClient):
    new_scooter = {
        "numero_serie": "STATUS-ERR",
        "modelo": "Test",
        "bateria": 50,
        "estado": "volando",  # Estado no valido
        "zona_id": 1
    }
    response = client.post("/scooters/", json=new_scooter)
    # Pydantic v2 validará el Enum antes de llegar al CRUD si usamos el esquema correctamente en main.py
    # En este caso, schemas.ScooterCreate usa ScooterStatus Enum.
    assert response.status_code == 422 # Error de validacion de FastAPI/Pydantic

def test_delete_non_existent_zone(client: TestClient):
    response = client.delete("/zones/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Zona no encontrada"

def test_delete_non_existent_scooter(client: TestClient):
    response = client.delete("/scooters/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Patinete no encontrado"

def test_create_zone_missing_fields(client: TestClient):
    # Falta 'codigo_postal' que es obligatorio
    invalid_zone = {"nombre": "Incomplete"}
    response = client.post("/zones/", json=invalid_zone)
    assert response.status_code == 422

def test_create_scooter_duplicate_serial(client: TestClient):
    # S001 ya existe (seed)
    duplicate_scooter = {
        "numero_serie": "S001",
        "modelo": "Clone",
        "bateria": 50,
        "estado": "disponible",
        "zona_id": 1
    }
    response = client.post("/scooters/", json=duplicate_scooter)
    # Esto debería fallar por integridad en la BD (Unique constraint)
    # Dependiendo de como manejes el error en CRUD, aquí esperamos un error (500 o manejado)
    assert response.status_code >= 400

def test_auto_maintenance(client: TestClient):
    # Zona 1 ya tiene un patinete con 85% batería (conftest.py)
    # Creamos un patinete con 10% de batería en Zona 1
    scooter_low = {
        "numero_serie": "LOW-BATT",
        "modelo": "Test",
        "bateria": 10,
        "estado": "disponible",
        "zona_id": 1
    }
    client.post("/scooters/", json=scooter_low)
    
    # Ejecutamos mantenimiento
    response = client.post("/zones/1/mantenimiento")
    assert response.status_code == 200
    assert "Se han puesto 1 patinetes en mantenimiento" in response.json()["msg"]
    
    # Verificamos que el estado cambió
    resp_list = client.get("/scooters/")
    scooters = resp_list.json()
    found = False
    for s in scooters:
        if s["numero_serie"] == "LOW-BATT":
            assert s["estado"] == "mantenimiento"
            found = True
    assert found

def test_create_scooter_pydantic_battery_error(client: TestClient):
    # Tarea 4. Error 422 si pongo 150%
    new_scooter = {
        "numero_serie": "BATT-OVER",
        "modelo": "Test",
        "bateria": 150,
        "estado": "disponible",
        "zona_id": 1
    }
    response = client.post("/scooters/", json=new_scooter)
    assert response.status_code == 422 # Error de validacion de Pydantic