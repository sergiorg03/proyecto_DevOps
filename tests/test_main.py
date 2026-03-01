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

    # Creamos un patinete con 10% de batería en la zona seeded
    scooter_low = {
        "numero_serie": "LOW-BATT",
        "modelo": "Test",
        "bateria": 10,
        "estado": "disponible",
        "zona_id": zone_id
    }
    client.post("/scooters/", json=scooter_low)

    # Ejecutamos mantenimiento
    response = client.post(f"/zones/{zone_id}/mantenimiento")
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