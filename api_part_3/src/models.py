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

VALID_TOKENS = {
    "valid_doctor": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.doctor",
    "valid_nurse": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.nurse",
    "valid_admin": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.admin"
}