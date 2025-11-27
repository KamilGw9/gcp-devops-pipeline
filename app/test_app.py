import pytest
from main import app

@pytest.fixture
def client():
    """Tworzy test client dla Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ======== TESTY ========

def test_home(client):
    """Test endpointu /"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['service'] == 'Data Pipeline API'
    assert 'version' in data

def test_health(client):
    """Test endpointu /health"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

def test_transform_success(client):
    """Test transformacji danych"""
    response = client.post('/api/transform', 
        json={"name": "kamil", "age": "25"})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['transformed']['name'] == 'KAMIL'
    assert data['transformed']['age'] == 25

def test_transform_empty_json(client):
    """Test błędu gdy pusty JSON"""
    response = client.post('/api/transform', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_stats_empty(client):
    """Test statystyk bez danych"""
    response = client.get('/api/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_records' in data
    assert 'avg_age' in data or 'message' in data
