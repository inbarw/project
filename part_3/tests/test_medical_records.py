import pytest
import allure
import time

from part_3.src.models import VALID_TOKENS

VALID_PATIENT_ID = "P12345"
VALID_PATIENT_NAME = "John Doe"
VALID_PATIENT_DOB = "1980-01-01"

@pytest.mark.parametrize(
    "endpoint, headers, expected_status, expected_detail",
    [
        (f"/patients/{VALID_PATIENT_ID}/records", {"Authorization": f"Bearer {VALID_TOKENS['valid_doctor']}"}, 200, None),  # Valid token
        (f"/patients/{VALID_PATIENT_ID}/records", {}, 403, "Not authenticated"),  # No token
        (f"/patients/{VALID_PATIENT_ID}/records", {"Authorization": "Bearer invalid_token_123"}, 401, "Invalid authentication token"),  # Invalid token
        (f"/patients/{VALID_PATIENT_ID}/records", {"Authorization": "InvalidTokenFormat"}, 403, "Not authenticated"),  # Malformed token
    ],
)
@allure.title("Test various authentication scenarios")
def test_authentication(api_client, endpoint, headers, expected_status, expected_detail):
    """Test various authentication scenarios."""
    with allure.step("Send GET request to retrieve patient records"):
        response = api_client.get(endpoint, headers=headers)

    with allure.step("Verify response status code"):
        assert response.status_code == expected_status

    if expected_detail:
        with allure.step("Verify response detail message"):
            assert expected_detail.lower() in response.json()["detail"].lower()


@pytest.mark.parametrize(
    "patient_id, expected_status, expected_detail",
    [
        (VALID_PATIENT_ID, 200, None),  # Valid ID
        ("11", 404, "Patient not found"),  # Non-existent ID
        ("' OR 1=1", 400, "Invalid patient ID format"),  # SQL Injection-like input
        ("error", 500, "Database error"),  # Simulated database error
    ],
)
@allure.title("Test error handling for various patient IDs")
def test_patient_records_error_handling(api_client, valid_headers, patient_id, expected_status, expected_detail):
    """Test error handling for various patient IDs."""
    with allure.step(f"Send GET request for patient ID: {patient_id}"):
        response = api_client.get(f"/patients/{patient_id}/records", headers=valid_headers)

    with allure.step("Verify response status code"):
        assert response.status_code == expected_status

    if expected_detail:
        with allure.step("Verify response detail message"):
            assert response.json()["detail"] == expected_detail

@allure.title("Test API response time for retrieving patient records")
def test_response_time(api_client, valid_headers):
    """Test API response time for retrieving patient records."""
    with allure.step("Send GET request and measure response time"):
        start_time = time.time()
        response = api_client.get(f"/patients/{VALID_PATIENT_ID}/records", headers=valid_headers)
        end_time = time.time()

    with allure.step("Verify response time and status"):
        assert response.status_code == 200
        response_time = end_time - start_time
        allure.attach(
            str(response_time),
            name="Response Time (seconds)",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert response_time < 1.0

@allure.title("Test access with different role tokens")
@pytest.mark.parametrize("role", ["valid_admin", "valid_nurse", "valid_doctor"])
def test_different_roles_access(api_client, role):
    """Test access with different role tokens."""
    with allure.step(f"Send GET request with {role} token"):
        token = VALID_TOKENS.get(role)  # Get the corresponding token for each role
        headers = {"Authorization": f"Bearer {token}"}
        response = api_client.get(f"/patients/{VALID_PATIENT_ID}/records", headers=headers)

    with allure.step(f"Verify response status for role {role}"):
        assert response.status_code == 200, f"Access failed for role: {role}"

@allure.title("Test response data structure for retrieving patient records")
def test_response_data_structure(api_client, valid_headers):
    """
    Test the correctness of the response data structure for a valid request.
    """
    with allure.step("Send GET request to retrieve patient records"):
        response = api_client.get(f"/patients/{VALID_PATIENT_ID}/records", headers=valid_headers)

    with allure.step("Verify response status code"):
        assert response.status_code == 200, "Unexpected status code"

    with allure.step("Verify response data structure"):
        data = response.json()
        assert "patient" in data, "'patient' key missing in response"
        assert "records" in data, "'records' key missing in response"

        patient = data["patient"]
        assert patient["id"] == VALID_PATIENT_ID, "Incorrect patient ID"
        assert patient["name"] == VALID_PATIENT_NAME, "Incorrect patient name"
        assert patient["dateOfBirth"] == VALID_PATIENT_DOB, "Incorrect patient date of birth"