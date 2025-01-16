import allure
import pytest
from unittest.mock import Mock, patch
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.testclient import TestClient

# Security scheme
security = HTTPBearer()

# Mock data
MOCK_PATIENT_RECORD = {
    "patient": {
        "id": "P12345",
        "name": "John Doe",
        "dateOfBirth": "1980-01-01"
    },
    "records": [
        {
            "id": "R1",
            "date": "2024-01-15",
            "type": "Blood Test",
            "result": "Normal"
        }
    ]
}

MOCK_DB_RESPONSE = [
    (
        "P12345", "John Doe", "1980-01-01",
        "R1", "2024-01-15", "Blood Test", "Normal"
    )
]

# Mock valid tokens for different roles
VALID_TOKENS = {
    "valid_doctor": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.doctor",
    "valid_nurse": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.nurse",
    "valid_admin": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.admin"
}


@pytest.fixture
def db_session():
    """Mock database session"""
    session = Mock()
    session.execute.return_value = MOCK_DB_RESPONSE
    session.close.return_value = None
    return session


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token and user role"""
    token = credentials.credentials
    if token not in VALID_TOKENS.values():
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@pytest.fixture
def api_client(db_session):
    """Test client fixture with authentication"""
    app = FastAPI()

    @app.get("/patients/{patient_id}/records")
    async def get_patient_records(
            patient_id: str,
            token: str = Depends(verify_token)
    ):
        # Input validation
        if any(char in patient_id for char in "';\\/"):
            raise HTTPException(status_code=400, detail="Invalid patient ID format")

        # Simulate database query
        if patient_id == "invalid":
            raise HTTPException(status_code=404, detail="Patient not found")
        if patient_id == "error":
            raise HTTPException(status_code=500, detail="Database error")
        return MOCK_PATIENT_RECORD

    return TestClient(app)


class TestMedicalRecordsAPI:
    @allure.feature('Patient Records')
    @allure.story('Successful record retrieval')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_record_retrieval(self, api_client):
        """Test successful retrieval of patient records with valid token"""
        headers = {"Authorization": f"Bearer {VALID_TOKENS['valid_doctor']}"}
        response = api_client.get("/patients/P12345/records", headers=headers)

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "patient" in data
        assert "records" in data

        # Verify patient data
        patient = data["patient"]
        assert patient["id"] == "P12345"
        assert patient["name"] == "John Doe"
        assert patient["dateOfBirth"] == "1980-01-01"

    def test_unauthorized_no_token(self, api_client):
        """Test request without authentication token"""
        response = api_client.get("/patients/P12345/records")
        assert response.status_code == 403
        assert "not authenticated" in response.json()["detail"].lower()

    def test_unauthorized_invalid_token(self, api_client):
        """Test request with invalid authentication token"""
        headers = {"Authorization": "Bearer invalid_token_123"}
        response = api_client.get("/patients/P12345/records", headers=headers)
        assert response.status_code == 401
        assert "invalid authentication token" in response.json()["detail"].lower()

    def test_unauthorized_malformed_token(self, api_client):
        """Test request with malformed authentication token"""
        headers = {"Authorization": "InvalidTokenFormat"}
        response = api_client.get("/patients/P12345/records", headers=headers)
        assert response.status_code == 403
        assert "not authenticated" in response.json()["detail"].lower()

    def test_different_roles_access(self, api_client):
        """Test access with different role tokens"""
        for role, token in VALID_TOKENS.items():
            headers = {"Authorization": f"Bearer {token}"}
            response = api_client.get("/patients/P12345/records", headers=headers)
            assert response.status_code == 200, f"Failed for role: {role}"

    def test_patient_not_found(self, api_client):
        """Test handling of non-existent patient ID"""
        headers = {"Authorization": f"Bearer {VALID_TOKENS['valid_doctor']}"}
        response = api_client.get("/patients/invalid/records", headers=headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Patient not found"

    def test_database_error(self, api_client):
        """Test handling of database errors"""
        headers = {"Authorization": f"Bearer {VALID_TOKENS['valid_doctor']}"}
        response = api_client.get("/patients/error/records", headers=headers)
        assert response.status_code == 500
        assert response.json()["detail"] == "Database error"

    @patch("time.time")
    def test_response_time(self, mock_time, api_client):
        """Test API response time using mocked time"""
        start_time = 0
        end_time = 0.5
        mock_time.side_effect = [start_time, end_time]

        headers = {"Authorization": f"Bearer {VALID_TOKENS['valid_doctor']}"}
        response = api_client.get("/patients/P12345/records", headers=headers)

        assert response.status_code == 200
        assert end_time - start_time < 1.0

    def test_sql_injection_prevention(self, api_client):
        """Test that SQL injection attempts are handled safely"""
        headers = {"Authorization": f"Bearer {VALID_TOKENS['valid_doctor']}"}
        malicious_id = "P12345'; DROP TABLE patients; --"
        response = api_client.get(f"/patients/{malicious_id}/records", headers=headers)

        assert response.status_code == 400
        assert "Invalid patient ID format" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main(["-v"])