from app.core.security import get_current_user
from fastapi import APIRouter, Depends

from app.api.v1.routes import (
    auth,
    user,
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
    media_type,
)

routers = [
    (auth.router, "/auth", "Auth", []),
    (user.router, "/users", "Users", [Depends(get_current_user)]),
    (county.router, "/counties", "Counties", []),
    (sub_county.router, "/sub-counties", "Sub Counties", []),
    (medical_facility.router, "/medical-facilities", "Medical Facilities", []),
    (gender.router, "/genders", "Genders", []),
    (level.router, "/levels", "Levels", []),
    (patient.router, "/patients", "Patients", [Depends(get_current_user)]),
    (encounter_assessment.router, "/encounter-assessments", "Encounter Assessments", [Depends(get_current_user)]),
    (referral.router, "/referrals", "Referrals", [Depends(get_current_user)]),
    (follow_up_status.router, "/follow-up-statuses", "Follow-Up Statuses", []),
    (follow_up.router, "/follow-ups", "Follow-Ups", [Depends(get_current_user)]),
    (document_category.router, "/document-categories", "Document Categories", []),
    (media_type.router, "/media-types", "Media Types", []),
]

api_router = APIRouter()

for route, prefix, tags, dependencies in routers:
    api_router.include_router(route, prefix=prefix, tags=tags, dependencies=dependencies)