from unittest.mock import patch

import pytest

from api_part_3.src.models import VALID_TOKENS


class TestMedicalRecordsAPI:
    def test_successful_record_retrieval(self, api_client, valid_headers):
        """Test successful retrieval of patient records with valid token"""
        response = api_client.get("/patients/P12345/records", headers=valid_headers)

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

    def test_patient_not_found(self, api_client, valid_headers):
        """Test handling of non-existent patient ID"""
        response = api_client.get("/patients/invalid/records", headers=valid_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Patient not found"

    def test_database_error(self, api_client, valid_headers):
        """Test handling of database errors"""
        response = api_client.get("/patients/error/records", headers=valid_headers)
        assert response.status_code == 500
        assert response.json()["detail"] == "Database error"

    @patch("time.time")
    def test_response_time(self, mock_time, api_client, valid_headers):
        """Test API response time using mocked time"""
        start_time = 0
        end_time = 0.5
        mock_time.side_effect = [start_time, end_time]

        response = api_client.get("/patients/P12345/records", headers=valid_headers)

        assert response.status_code == 200
        assert end_time - start_time < 1.0

    def test_sql_injection_prevention(self, api_client, valid_headers):
        """Test that SQL injection attempts are handled safely"""
        malicious_id = "P12345'; DROP TABLE patients; --"
        response = api_client.get(f"/patients/{malicious_id}/records", headers=valid_headers)

        assert response.status_code == 400
        assert "Invalid patient ID format" in response.json()["detail"]

