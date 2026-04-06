from app.api.v1.routes import (
    auth,
    county,
    sub_county,
    medical_facility,
    gender,
    level,
    patient,
    encounter_assessment,
    referral,
    follow_up_status,
    follow_up,
    document_category,
    media_type
)
from app.db import events  # noqa
from fastapi import FastAPI

app = FastAPI()
app.include_router(auth.router)
app.include_router(county.router)
app.include_router(sub_county.router)
app.include_router(medical_facility.router)
app.include_router(gender.router)
app.include_router(level.router)
app.include_router(patient.router)
app.include_router(encounter_assessment.router)
app.include_router(referral.router)
app.include_router(follow_up_status.router)
app.include_router(follow_up.router)
app.include_router(document_category.router)
app.include_router(media_type.router)