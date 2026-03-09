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

def test_zone_mantenimiento(client: TestClient):
    '''
        Test para el mantenimiento automatico de zonas
    '''
    zone_id = pytest.seeded_zone_id
    
    # Creamos un scooter con batería baja (< 15%) para que el mantenimiento lo afecte
    new_scooter = {
        "numero_serie": "chami",
        "modelo": "Test",
        "bateria": 10,
        "estado": "disponible",
        "zona_id": zone_id
    }
    client.post("/scooters/", json=new_scooter)

    # Llamada a mantenimiento
    response = client.post(f"/zones/{zone_id}/mantenimiento")
    assert response.status_code == 200
    
    # Verificar que los scooters de la zona con batería < 15 estén en mantenimiento
    scooters = client.get("/scooters/").json()
    for s in scooters:
        if s["zona_id"] == zone_id:
            if s["bateria"] < 15:
                assert s["estado"] == "mantenimiento"
            else:
                # El scooter original tiene 85%, no debería estar en mantenimiento
                assert s["estado"] != "mantenimiento"

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
        Comprobacion de valores de bateria en los rangos correctos
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
    assert "bateria" in str(response_high.json()["detail"])

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
    assert "bateria" in str(response_low.json()["detail"])

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
