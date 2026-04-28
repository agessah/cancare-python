from fastapi import HTTPException, Request

from app.db.enums.ConsultationStatus import ConsultationStatus
from app.repositories import TeleConsultationRepository, PatientRepository


class TeleConsultationService:
    def __init__(
            self,
            repo: TeleConsultationRepository,
            patient_repo: PatientRepository,
    ):
        self.repo = repo
        self.patient_repo = patient_repo

    async def create(self, payload, current_user):
        patient = await self.patient_repo.get(payload.patient_id)
        if not patient:
            raise HTTPException(404, "Selected patient not found!")

        data = payload.model_dump()
        data['chw_id'] = current_user.id
        data['oncologist_id'] = None
        data['response'] = None
        data["status"] = ConsultationStatus.SENT

        return await self.repo.create(data)


    async def update(self, resource_id, payload, current_user):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(404, "Tele consultation not found!")

        data = payload.model_dump(exclude_unset=True)
        data['oncologist_id'] = current_user.id
        data["status"] = ConsultationStatus.REVIEWED

        return await self.repo.update(resource_id, data)


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
            raise HTTPException(status_code=404, detail="Record not found!")

        return resource