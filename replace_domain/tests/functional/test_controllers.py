from fastapi.testclient import TestClient


def test_read_health(client: TestClient) -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'data': {'is_healthy': True, 'postgresql': 'OK', 'redis': 'OK'}}


def test_head_health(client: TestClient) -> None:
    response = client.head('/health/')
    assert response.status_code == 200
