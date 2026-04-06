from app.core.security import get_current_user  # your auth function
from app.db.events import current_user_id
from app.db.session import get_db
from app.repositories import (
    FollowUpStatusRepository,
    CountyRepository,
    DocumentCategoryRepository,
    EncounterAssessmentRepository,
    GenderRepository,
    LevelRepository,
    MediaTypeRepository,
    MedicalFacilityRepository,
    PatientRepository,
    ReferralRepository,
    SubCountyRepository, FollowUpRepository
)
from app.services import (
    CountyService,
    DocumentCategoryService,
    EncounterAssessmentService,
    FollowUpStatusService,
    GenderService,
    LevelService,
    MediaTypeService,
    MedicalFacilityService,
    PatientService,
    ReferralService,
    SubCountyService
)
from app.services.email_service import EmailService
from app.services.follow_up import FollowUpService

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


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

def get_medical_facility_service(
    db: AsyncSession = Depends(get_db),
):
    repo = MedicalFacilityRepository(db)
    return MedicalFacilityService(repo)

def get_gender_service(
    db: AsyncSession = Depends(get_db),
):
    repo = GenderRepository(db)
    return GenderService(repo)

def get_level_service(
    db: AsyncSession = Depends(get_db),
):
    repo = LevelRepository(db)
    return LevelService(repo)

def get_follow_up_status_service(
    db: AsyncSession = Depends(get_db),
):
    repo = FollowUpStatusRepository(db)
    return FollowUpStatusService(repo)

def get_document_category_service(
    db: AsyncSession = Depends(get_db),
):
    repo = DocumentCategoryRepository(db)
    return DocumentCategoryService(repo)

def get_media_type_service(
    db: AsyncSession = Depends(get_db),
):
    repo = MediaTypeRepository(db)
    return MediaTypeService(repo)

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

def get_referral_service(
    db: AsyncSession = Depends(get_db),
):
    repo = ReferralRepository(db)
    return ReferralService(repo)

def get_follow_up_service(
    db: AsyncSession = Depends(get_db),
):
    repo = FollowUpRepository(db)
    return FollowUpService(repo)

def get_email_service():
    return EmailService()