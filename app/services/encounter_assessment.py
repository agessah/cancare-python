from app.repositories import EncounterAssessmentRepository, PatientRepository
from app.services.utils import UtilsService
from fastapi import HTTPException, Request


class EncounterAssessmentService:
    def __init__(
        self,
        repo: EncounterAssessmentRepository,
        patient_repo: PatientRepository,
        utils: UtilsService
    ):
        self.repo = repo
        self.patient_repo = patient_repo
        self.utils = utils

    async def create(self, payload):
        patient = await self.patient_repo.get(payload.patient_id)
        if not patient:
            raise HTTPException(404, "Selected patient not found!")

        age = self.utils.get_age(patient.date_of_birth)
        above_fifty = age >= 50

        data = payload.model_dump()
        data["age"] = age
        data["above_fifty"] = above_fifty

        return await self.repo.create(data)

    async def update(self, resource_id, payload):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(404, "Encounters assessment not found!")

        return await self.repo.update(resource_id, payload.model_dump(exclude_unset=True))

    async def index(
        self,
        request: Request,
        search: str = None,
        sort: str = None,
        filters: dict = None
    ):
        return await self.repo.index(
            request=request,
            search=search,
            sort=sort,
            filters=filters
        )

    async def show(self, resource_id: int):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(status_code=404, detail="Encounter assessment not found!")

        return resource