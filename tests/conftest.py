import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.config.config import Settings

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def test_settings():
    # Test-specific settings
    return Settings(
        UPLOAD_FOLDER="test_uploads",
        API_KEY="test-gemini-key"
    )

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Create test upload directory
    os.makedirs("test_uploads", exist_ok=True)
    
    yield
    
    # Teardown: Clean up test files
    for file in os.listdir("test_uploads"):
        os.remove(os.path.join("test_uploads", file))
    os.rmdir("test_uploads") 