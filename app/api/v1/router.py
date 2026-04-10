from fastapi import APIRouter

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
    (auth.router, "/auth", "Auth"),
    (user.router, "/users", "Users"),
    (county.router, "/counties", "Counties"),
    (sub_county.router, "/sub-counties", "Sub Counties"),
    (medical_facility.router, "/medical-facilities", "Medical Facilities"),
    (gender.router, "/genders", "Genders"),
    (level.router, "/levels", "Levels"),
    (patient.router, "/patients", "Patients"),
    (encounter_assessment.router, "/encounter-assessments", "Encounter Assessments"),
    (referral.router, "/referrals", "Referrals"),
    (follow_up_status.router, "/follow-up-statuses", "Follow-Up Statuses"),
    (follow_up.router, "/follow-ups", "Follow-Ups"),
    (document_category.router, "/document-categories", "Document Categories"),
    (media_type.router, "/media-types", "Media Types"),
]

api_router = APIRouter()

for route, prefix, tags in routers:
    api_router.include_router(route, prefix=prefix, tags=tags)