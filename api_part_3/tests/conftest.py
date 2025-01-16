import pytest
from fastapi.testclient import TestClient
from api_part_3.src.app import create_app
from api_part_3.src.models import VALID_TOKENS


@pytest.fixture
def api_client():
    app = create_app()
    return TestClient(app)

@pytest.fixture
def valid_headers():
    return {"Authorization": f"Bearer {VALID_TOKENS['valid_doctor']}"}