"""Unit tests for Data Pipeline API."""

import pytest
from main import app


@pytest.fixture
def client():
    """Create Flask test client with testing mode enabled."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHomeEndpoint:
    """Tests for the root endpoint."""
    
    def test_returns_api_info(self, client):
        """GET / should return service name and version."""
        response = client.get('/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['service'] == 'Data Pipeline API'
        assert 'version' in data


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_returns_healthy_status(self, client):
        """GET /health should return healthy status with timestamp."""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data


class TestTransformEndpoint:
    """Tests for the data transformation endpoint."""
    
    def test_transforms_valid_data(self, client):
        """POST /api/transform should uppercase name and convert age to int."""
        response = client.post('/api/transform', 
            json={"name": "kamil", "age": "25"})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['transformed']['name'] == 'KAMIL'
        assert data['transformed']['age'] == 25
    
    def test_rejects_empty_payload(self, client):
        """POST /api/transform with empty JSON should return 400 error."""
        response = client.post('/api/transform', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestStatsEndpoint:
    """Tests for the statistics endpoint."""
    
    def test_returns_statistics(self, client):
        """GET /api/stats should return record count and age statistics."""
        response = client.get('/api/stats')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_records' in data
        assert 'avg_age' in data or 'message' in data
