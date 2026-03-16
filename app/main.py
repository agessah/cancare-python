from fastapi import FastAPI
from app.api.v1.routes import auth, county, sub_county, gender, patient, encounter_assessment
from app.db import events  # noqa

app = FastAPI()
app.include_router(auth.router)
app.include_router(county.router)
app.include_router(sub_county.router)
app.include_router(gender.router)
app.include_router(patient.router)
app.include_router(encounter_assessment.router)