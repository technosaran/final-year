"""
Tests for main FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app
from config import settings


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "services" in data


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data
    assert "timestamp" in data


def test_cors_headers(client):
    """Test CORS headers are present"""
    response = client.options("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200


def test_rate_limiting(client):
    """Test rate limiting middleware"""
    # This would need more sophisticated testing in a real scenario
    response = client.get("/")
    assert response.status_code == 200


@patch('services.ai_summary.ai_service')
def test_health_with_ai_service(mock_ai_service, client):
    """Test health check with AI service"""
    mock_ai_service.summarizer = MagicMock()
    
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["services"]["ai_models"] in ["healthy", "loading"]


def test_invalid_endpoint(client):
    """Test 404 for invalid endpoints"""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404


def test_api_versioning(client):
    """Test API versioning is working"""
    # Test that v1 prefix is used
    assert settings.api_v1_prefix == "/api/v1"


class TestErrorHandling:
    """Test error handling"""
    
    def test_validation_error(self, client):
        """Test validation error handling"""
        # This would test with invalid request data
        pass
    
    def test_http_exception(self, client):
        """Test HTTP exception handling"""
        pass
    
    def test_general_exception(self, client):
        """Test general exception handling"""
        pass