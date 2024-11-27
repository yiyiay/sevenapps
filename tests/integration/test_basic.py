import pytest
from sevenapps import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_basic_integration(client):
    """Test basic application integration"""
    response = client.get('/')
    assert response.status_code == 200 