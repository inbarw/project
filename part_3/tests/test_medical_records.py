import allure
from unittest.mock import patch
from part_3.src.models import VALID_TOKENS

allure.epic("Medical Records API")
@allure.feature("Patient Records Management")
class TestMedicalRecordsAPI:

    @allure.story("Authentication and Authorization")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_record_retrieval(self, api_client, valid_headers):
        """Test successful retrieval of patient records with valid token"""
        with allure.step("Send GET request to retrieve patient records"):
            response = api_client.get("/patients/P12345/records", headers=valid_headers)

        with allure.step("Verify response status code"):
            assert response.status_code == 200

        with allure.step("Verify response data structure"):
            data = response.json()
            assert "patient" in data
            assert "records" in data

        with allure.step("Verify patient data"):
            patient = data["patient"]
            assert patient["id"] == "P12345"
            assert patient["name"] == "John Doe"
            assert patient["dateOfBirth"] == "1980-01-01"

    @allure.story("Authentication and Authorization")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_unauthorized_no_token(self, api_client):
        """Test request without authentication token"""
        with allure.step("Send GET request without token"):
            response = api_client.get("/patients/P12345/records")

        with allure.step("Verify unauthorized response"):
            assert response.status_code == 403
            assert "not authenticated" in response.json()["detail"].lower()

    @allure.story("Authentication and Authorization")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_unauthorized_invalid_token(self, api_client):
        """Test request with invalid authentication token"""
        with allure.step("Send GET request with invalid token"):
            headers = {"Authorization": "Bearer invalid_token_123"}
            response = api_client.get("/patients/P12345/records", headers=headers)

        with allure.step("Verify unauthorized response"):
            assert response.status_code == 401
            assert "invalid authentication token" in response.json()["detail"].lower()

    @allure.story("Authentication and Authorization")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_unauthorized_malformed_token(self, api_client):
        """Test request with malformed authentication token"""
        with allure.step("Send GET request with malformed token"):
            headers = {"Authorization": "InvalidTokenFormat"}
            response = api_client.get("/patients/P12345/records", headers=headers)

        with allure.step("Verify unauthorized response"):
            assert response.status_code == 403
            assert "not authenticated" in response.json()["detail"].lower()

    @allure.story("Authentication and Authorization")
    @allure.severity(allure.severity_level.NORMAL)
    def test_different_roles_access(self, api_client):
        """Test access with different role tokens"""
        for role, token in VALID_TOKENS.items():
            with allure.step(f"Send GET request with {role} token"):
                headers = {"Authorization": f"Bearer {token}"}
                response = api_client.get("/patients/P12345/records", headers=headers)

            with allure.step(f"Verify response status for role {role}"):
                assert response.status_code == 200, f"Failed for role: {role}"

    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    def test_patient_not_found(self, api_client, valid_headers):
        """Test handling of non-existent patient ID"""
        with allure.step("Send GET request with non-existent patient ID"):
            response = api_client.get("/patients/invalid/records", headers=valid_headers)

        with allure.step("Verify patient not found response"):
            assert response.status_code == 404
            assert response.json()["detail"] == "Patient not found"

    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    def test_database_error(self, api_client, valid_headers):
        """Test handling of database errors"""
        with allure.step("Send GET request to simulate database error"):
            response = api_client.get("/patients/error/records", headers=valid_headers)

        with allure.step("Verify database error response"):
            assert response.status_code == 500
            assert response.json()["detail"] == "Database error"

    @allure.story("Performance")
    @allure.severity(allure.severity_level.NORMAL)
    @patch("time.time")
    def test_response_time(self, mock_time, api_client, valid_headers):
        """Test API response time using mocked time"""
        start_time = 0
        end_time = 0.5
        mock_time.side_effect = [start_time, end_time, end_time + 1]

        with allure.step("Send GET request and measure response time"):
            response = api_client.get("/patients/P12345/records", headers=valid_headers)

        with allure.step("Verify response time is within acceptable range"):
            assert response.status_code == 200
            response_time = end_time - start_time
            allure.attach(
                str(response_time),
                name="Response Time (seconds)",
                attachment_type=allure.attachment_type.TEXT
            )
            assert response_time < 1.0

    @allure.story("Security")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sql_injection_prevention(self, api_client, valid_headers):
        """Test that SQL injection attempts are handled safely"""
        with allure.step("Send GET request with malicious SQL injection"):
            malicious_id = "P12345'; DROP TABLE patients; --"
            response = api_client.get(f"/patients/{malicious_id}/records", headers=valid_headers)

        with allure.step("Verify request is rejected"):
            assert response.status_code == 400
            assert "Invalid patient ID format" in response.json()["detail"]
