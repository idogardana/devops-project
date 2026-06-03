import pytest
from app import app

# פיקסטורה שמייצרת לקוח בדיקות זמני של Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# טסט עבור הנתיב הראשי /
def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "1.0"}

# test עבור נתיב ה-Health Check
def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}