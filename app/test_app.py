"""Tests for Crypto Tracker API."""
import pytest
import os

# Set env var to skip DB init during import
os.environ["SKIP_DB_INIT"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
    with app.test_client() as client:
        yield client
        
    with app.app_context():
        db.drop_all()


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