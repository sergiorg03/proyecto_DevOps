import pytest
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
    zone_id = pytest.seeded_zone_id
    response = client.get(f"/zones/{zone_id}")
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
    zone_id = pytest.seeded_zone_id
    response = client.delete(f"/zones/{zone_id}")
    assert response.status_code == 200
    assert response.json() == {"msg": "Zona eliminada"}

    # Verificar que ya no existe
    get_resp = client.get(f"/zones/{zone_id}")
    assert get_resp.status_code == 404

def test_delete_zone_cascade(client: TestClient):
    zone_id = pytest.seeded_zone_id
    scooter_id = pytest.seeded_scooter_id

    # Verificación de existencia del scooter
    check_scooter = client.get(f"/scooters/{scooter_id}")
    assert check_scooter.status_code == 200

    # Eliminamos la zona
    client.delete(f"/zones/{zone_id}")

    # Verificación de existencia en la BD (debe haber desaparecido en cascada)
    check_scooter_deleted = client.get(f"/scooters/{scooter_id}")
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
        "zona_id": pytest.seeded_zone_id
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
        "zona_id": 999999
    }
    response = client.post("/scooters/", json=new_scooter)
    assert response.status_code == 404
    assert response.json()["detail"] == "Zona no encontrada"

def test_update_zone_corr(client: TestClient):
    """Actualización completa de una zona."""
    zone_id = pytest.seeded_zone_id
    update_data = {"nombre": "Zona Actualizada", "codigo_postal": 28002, "limite_velocidad": 30}
    response = client.put(f"/zones/{zone_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Zona Actualizada"
    assert data["codigo_postal"] == 28002
    assert data["limite_velocidad"] == 30

def test_update_zone_not_found_incorr(client: TestClient):
    """Intentar actualizar una zona que no existe."""
    response = client.put("/zones/999999", json={"nombre": "No Existe"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Zona no encontrada"

def test_update_zone_velocidad_incorr(client: TestClient):
    """Intentar actualizar con límite de velocidad negativo."""
    zone_id = pytest.seeded_zone_id
    response = client.put(f"/zones/{zone_id}", json={"limite_velocidad": -5})
    assert response.status_code == 422
    assert "límite de velocidad no puede ser negativo" in response.json()["detail"][0]["msg"]

'''
    TEST SCOOTERS
'''

def test_get_scooters_corr(client: TestClient):
    response = client.get("/scooters/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_scooter_id_corr(client: TestClient):
    scooter_id = pytest.seeded_scooter_id
    response = client.get(f"/scooters/{scooter_id}")
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
        "zona_id": pytest.seeded_zone_id
    }
    response = client.post("/scooters/", json=new_scooter)
    assert response.status_code == 200
    data = response.json()
    assert data["numero_serie"] == "TEST-001"

def test_delete_scooter(client: TestClient):
    scooter_id = pytest.seeded_scooter_id
    response = client.delete(f"/scooters/{scooter_id}")
    assert response.status_code == 200
    assert response.json() == {"msg": "Patinete eliminado"}

    # Verificación de existencia en la BD
    get_resp = client.get(f"/scooters/{scooter_id}")
    assert get_resp.status_code == 404

def test_create_scooter_incorr(client: TestClient):
    new_scooter = {
        "numero_serie": "STATUS-ERR",
        "modelo": "Test",
        "bateria": 50,
        "estado": "volando",  # Estado no válido
        "zona_id": pytest.seeded_zone_id
    }
    response = client.post("/scooters/", json=new_scooter)
    assert response.status_code == 422  # Error de validación de FastAPI/Pydantic

def test_delete_non_existent_zone(client: TestClient):
    response = client.delete("/zones/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Zona no encontrada"

def test_delete_non_existent_scooter(client: TestClient):
    response = client.delete("/scooters/999999")
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
        "zona_id": pytest.seeded_zone_id
    }
    response = client.post("/scooters/", json=duplicate_scooter)
    # Falla por Unique constraint en BD
    assert response.status_code >= 400

def test_auto_maintenance(client: TestClient):
    zone_id = pytest.seeded_zone_id

    # Creamos varios patinetes con batería baja (<15%) en la zona
    scooters_baja_bateria = [
        {"numero_serie": "LOW-BATT-1", "modelo": "Test", "bateria": 10, "estado": "disponible", "zona_id": zone_id},
        {"numero_serie": "LOW-BATT-2", "modelo": "Test", "bateria": 5, "estado": "disponible", "zona_id": zone_id},
        {"numero_serie": "LOW-BATT-3", "modelo": "Test", "bateria": 0, "estado": "en_uso", "zona_id": zone_id},
    ]
    for s in scooters_baja_bateria:
        client.post("/scooters/", json=s)

    # Creamos un patinete con batería suficiente (NO debe cambiar)
    scooter_ok = {"numero_serie": "HIGH-BATT", "modelo": "Test", "bateria": 80, "estado": "disponible", "zona_id": zone_id}
    client.post("/scooters/", json=scooter_ok)

    # Ejecutamos mantenimiento
    response = client.post(f"/zones/{zone_id}/mantenimiento")
    assert response.status_code == 200
    assert "Se han puesto 3 patinetes en mantenimiento" in response.json()["msg"]

    # Verificamos que TODOS los de batería baja están en mantenimiento
    resp_list = client.get("/scooters/")
    scooters = resp_list.json()

    series_baja = {"LOW-BATT-1", "LOW-BATT-2", "LOW-BATT-3"}
    for s in scooters:
        if s["numero_serie"] in series_baja:
            assert s["estado"] == "mantenimiento", f"{s['numero_serie']} debería estar en mantenimiento"

    # Verificamos que el de batería alta NO cambió
    for s in scooters:
        if s["numero_serie"] == "HIGH-BATT":
            assert s["estado"] == "disponible", "HIGH-BATT no debería estar en mantenimiento"

def test_update_scooter(client: TestClient):
    """Actualización completa de un patinete."""
    scooter_id = pytest.seeded_scooter_id
    update_data = {
        "numero_serie": "S001-UPD",
        "modelo": "Xiaomi Pro 2",
        "bateria": 95,
        "estado": "en_uso",
        "puntuacion_usuario": 4.5
    }
    response = client.put(f"/scooters/{scooter_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["numero_serie"] == "S001-UPD"
    assert data["modelo"] == "Xiaomi Pro 2"
    assert data["bateria"] == 95
    assert data["estado"] == "en_uso"
    assert data["puntuacion_usuario"] == 4.5

def test_update_scooter_partial(client: TestClient):
    """Actualización parcial: solo la batería."""
    scooter_id = pytest.seeded_scooter_id
    response = client.put(f"/scooters/{scooter_id}", json={"bateria": 50})
    assert response.status_code == 200
    data = response.json()
    assert data["bateria"] == 50
    # Los demás campos deben mantener sus valores originales
    assert data["numero_serie"] == "S001"
    assert data["modelo"] == "Xiaomi M365"

def test_update_scooter_not_found(client: TestClient):
    """Intentar actualizar un patinete que no existe."""
    response = client.put("/scooters/999999", json={"bateria": 50})
    assert response.status_code == 404
    assert response.json()["detail"] == "Patinete no encontrado"

def test_update_scooter_invalid_battery(client: TestClient):
    """Intentar actualizar con batería fuera de rango."""
    scooter_id = pytest.seeded_scooter_id
    response = client.put(f"/scooters/{scooter_id}", json={"bateria": 150})
    assert response.status_code == 422
    assert "batería debe estar entre 0 y 100" in response.json()["detail"][0]["msg"]

def test_update_scooter_invalid_rating(client: TestClient):
    """Intentar actualizar con puntuación fuera de rango (0-5)."""
    scooter_id = pytest.seeded_scooter_id
    response = client.put(f"/scooters/{scooter_id}", json={"puntuacion_usuario": 7.0})
    assert response.status_code == 422
    assert "puntuación debe estar entre 0 y 5" in response.json()["detail"][0]["msg"]

def test_update_scooter_duplicate_serial(client: TestClient):
    """Intentar actualizar un patinete con un número de serie que ya existe."""
    # Crear segundo scooter
    new_scooter = {
        "numero_serie": "S002",
        "modelo": "Segway",
        "bateria": 70,
        "estado": "disponible",
        "zona_id": pytest.seeded_zone_id
    }
    client.post("/scooters/", json=new_scooter)

    # Intentar cambiar el número de serie del seeded scooter al que ya existe
    scooter_id = pytest.seeded_scooter_id
    response = client.put(f"/scooters/{scooter_id}", json={"numero_serie": "S002"})
    assert response.status_code == 400
    assert "número de serie ya existe" in response.json()["detail"]

def test_update_scooter_invalid_status(client: TestClient):
    """Intentar actualizar con un estado que no existe."""
    scooter_id = pytest.seeded_scooter_id
    response = client.put(f"/scooters/{scooter_id}", json={"estado": "volando"})
    assert response.status_code == 422  # Pydantic rechaza el enum inválido

def test_update_scooter_non_existent_zone(client: TestClient):
    """Intentar mover un patinete a una zona que no existe."""
    scooter_id = pytest.seeded_scooter_id
    response = client.put(f"/scooters/{scooter_id}", json={"zona_id": 999999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Zona no encontrada"