"""Tests for Crypto Tracker API."""
import pytest
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test home endpoint returns API info."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Crypto Tracker API' in response.data


def test_health(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_get_crypto_price(client):
    """Test getting crypto price."""
    response = client.get('/api/crypto/bitcoin')
    assert response.status_code == 200
    data = response.get_json()
    assert 'coin' in data
    assert 'prices' in data


def test_get_top10(client):
    """Test getting top 10 cryptos."""
    response = client.get('/api/crypto/top10')
    assert response.status_code == 200
    data = response.get_json()
    assert 'top_10' in data


def test_portfolio_empty(client):
    """Test empty portfolio."""
    response = client.get('/api/portfolio')
    assert response.status_code == 200


def test_alerts_empty(client):
    """Test empty alerts."""
    response = client.get('/api/alerts')
    assert response.status_code == 200
    data = response.get_json()
    assert 'alerts' in data