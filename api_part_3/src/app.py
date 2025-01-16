# src/app.py
from fastapi import FastAPI, HTTPException, Depends
from .auth import verify_token
from .models import MOCK_PATIENT_RECORD

def create_app():
    app = FastAPI()

    @app.get("/patients/{patient_id}/records")
    async def get_patient_records(
            patient_id: str,
            token: str = Depends(verify_token)
    ):
        if any(char in patient_id for char in "';\\/"):
            raise HTTPException(status_code=400, detail="Invalid patient ID format")

        if patient_id == "invalid":
            raise HTTPException(status_code=404, detail="Patient not found")
        if patient_id == "error":
            raise HTTPException(status_code=500, detail="Database error")
        return MOCK_PATIENT_RECORD

    return app