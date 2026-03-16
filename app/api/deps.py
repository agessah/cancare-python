from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user  # your auth function
from app.db.events import current_user_id
from app.db.session import get_db
from app.repositories.county import CountyRepository
from app.repositories.encounter_assessment import EncounterAssessmentRepository
from app.repositories.gender import GenderRepository
from app.repositories.patient import PatientRepository
from app.repositories.sub_county import SubCountyRepository
from app.services.county import CountyService
from app.services.encounter_assessment import EncounterAssessmentService
from app.services.gender import GenderService
from app.services.patient import PatientService
from app.services.sub_county import SubCountyService


def set_current_user(
    user=Depends(get_current_user),
):
    token = current_user_id.set(user.id)
    try:
        yield
    finally:
        current_user_id.reset(token)

def get_county_service(
    db: AsyncSession = Depends(get_db),
):
    repo = CountyRepository(db)
    return CountyService(repo)

def get_sub_county_service(
    db: AsyncSession = Depends(get_db),
):
    repo = SubCountyRepository(db)
    return SubCountyService(repo)

def get_gender_service(
    db: AsyncSession = Depends(get_db),
):
    repo = GenderRepository(db)
    return GenderService(repo)

def get_patient_service(
    db: AsyncSession = Depends(get_db),
):
    repo = PatientRepository(db)
    return PatientService(repo)

def get_encounter_assessment_service(
    db: AsyncSession = Depends(get_db),
):
    repo = EncounterAssessmentRepository(db)
    return EncounterAssessmentService(repo)