from fastapi.testclient import TestClient

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "API funcionando"}

def test_get_zones(client: TestClient):
    response = client.get("/zones/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_scooters(client: TestClient):
    response = client.get("/scooters/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
