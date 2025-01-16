import pytest
from part_3_api_tests.medical_data_api import app
import time


@pytest.fixture
def client():
    # This creates a test client to interact with your Flask app
    with app.test_client() as client:
        yield client

# def test_verify_patient_data(client):
#     response = client.get('/api/medical-records/1')
#     assert response.status_code == 200
#     response_json = response.get_json()
#     assert response_json['patient_id'] == 1
#     assert response_json['patient_name'] == "John Doe"
#     assert response_json['test_results'] == "Positive"
#
# def test_verify_response_time(client,):
#     start_time = time.time()
#     client.get('/api/medical-records/1')
#     response_time = time.time() - start_time
#     assert response_time < 1, f"Response time exceeded threshold: {response_time} seconds"
#
# def test_verify_patient_data_not_found(client, mocker):
#     mocker.patch('part_3_api_tests.medical_data_api.get_patient_data_from_db', return_value=None)
#     response = client.get('/api/medical-records/999')
#     assert response.status_code == 404
#     response_json = response.get_json()
#     assert response_json['error'] == "Patient not found"
#
# def test_unauthorized_request(client):
#     response = client.get('/api/medical-records/1')
#     assert response.status_code == 401
#     response_json = response.get_json()
#     assert response_json['error'] == "Unauthorized"

# def test_incorrect_patient_id(client):
#     response = client.get('/api/medical-records/invalud')
#     assert response.status_code == 400
#     response_json = response.get_json()
#     assert response_json['error'] == "Bad Request: Invalid patient ID"

def test_server_error(client, mocker):
    mocker.patch('part_3_api_tests.medical_data_api.get_patient_data_from_db', side_effect=Exception("Database failure"))
    response = client.get('/api/medical-records/1')
    assert response.status_code == 500
    response_json = response.get_json()
    assert response_json['error'] == "Internal Server Error: Database failure"
