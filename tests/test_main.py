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
    response = client.get("/zones/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Zona no encontrada"}

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
    response = client.get("/scooters/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Patinete no encontrado"}