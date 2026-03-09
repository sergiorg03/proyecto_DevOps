import pytest
from fastapi.testclient import TestClient

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "API funcionando"}

'''
    TEST ZONAS
'''
def test_create_zone(client: TestClient):
    '''
        Creacion de zonas 
    '''
    new_zone = {"nombre": "Test Zone", "codigo_postal": 28000, "limite_velocidad": 25}
    response = client.post("/zones/", json=new_zone)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Test Zone"
    assert "id" in data

def test_create_scooter_invalid_battery(client: TestClient):
    '''
        Test para la creacion de scooters con bateria incorrecta
    '''
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

'''
    TEST SCOOTERS
'''
def test_create_scooter(client: TestClient):
    '''
        Test cracion de scooters
    '''
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
    '''
        Borrado de scooters
    '''
    scooter_id = pytest.seeded_scooter_id
    response = client.delete(f"/scooters/{scooter_id}")
    assert response.status_code == 200
    assert response.json() == {"msg": "Patinete eliminado"}

    # Verificación de existencia en la BD
    get_resp = client.get(f"/scooters/{scooter_id}")
    assert get_resp.status_code == 404

def test_scooter_battery_validation(client: TestClient):
    """
    Verifica que la creación de un patinete falla si la batería
    es menor que 0 o mayor que 100.
    """

    # Batería demasiado alta
    scooter_high = {
        "numero_serie": "BAT-150",
        "modelo": "Test Model",
        "bateria": 150,          # inválido
        "estado": "disponible",
        "zona_id": pytest.seeded_zone_id
    }
    response_high = client.post("/scooters/", json=scooter_high)
    assert response_high.status_code == 422
    assert "batería" in str(response_high.json()["detail"])

    # Batería negativa
    scooter_low = {
        "numero_serie": "BAT--10",
        "modelo": "Test Model",
        "bateria": -10,          # inválido
        "estado": "disponible",
        "zona_id": pytest.seeded_zone_id
    }
    response_low = client.post("/scooters/", json=scooter_low)
    assert response_low.status_code == 422
    assert "batería" in str(response_low.json()["detail"])

    # Batería válida
    scooter_ok = {
        "numero_serie": "BAT-50",
        "modelo": "Test Model",
        "bateria": 50,           # válido
        "estado": "disponible",
        "zona_id": pytest.seeded_zone_id
    }
    response_ok = client.post("/scooters/", json=scooter_ok)
    assert response_ok.status_code == 200
    data = response_ok.json()
    assert data["bateria"] == 50
    assert data["numero_serie"] == "BAT-50"
