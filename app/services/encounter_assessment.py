import math
from pathlib import Path

import joblib
import numpy as np
from app.repositories import EncounterAssessmentRepository, PatientRepository
from app.services.utils import UtilsService
from fastapi import HTTPException, Request


class EncounterAssessmentService:
    model_path = Path(__file__).resolve().parents[1] / "ai" / "ultimate" / "best_model_randomforest.pkl"
    #feature_path = Path(__file__).resolve().parents[1] / "ai" / "ultimate" / "feature_columns.pkl"
    #encoder_path = Path(__file__).resolve().parents[1] / "ai" / "ultimate" / "label_encoder.pkl"

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


        # AI Analysis
        arr = self.numpy_array(data)
        model = joblib.load(self.model_path)

        pred = int(model.predict(arr)[0])
        prob = model.predict_proba(arr)[0]
        pred_prob = float(prob[int(pred)])

        interpreted = self.interpret_risk(pred_prob)

        # Save to db
        data["risk_score"] = pred_prob
        await self.repo.create(data)

        return {
            "score": int(math.floor((pred_prob * 100) + 0.5)),
            "label": interpreted.get("label"),
            "guidelines": interpreted.get("guidelines")
        }

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


    @staticmethod
    def numpy_array(data):
        return np.array([[
            data.get("age"),
            data.get("above_fifty"),
            data.get("painless_lump"),
            data.get("nipple_discharge"),
            data.get("skin_dimpling"),
            data.get("nipple_retraction"),
            data.get("redness_scaling"),
            data.get("breast_pain"),
            data.get("swollen_lymph_nodes"),
            data.get("family_history"),
            data.get("never_been_pregnant"),
            data.get("late_menopause"),
            data.get("bmi_risk"),
            data.get("alcohol_risk"),
            data.get("smoker"),
            data.get("low_physical_activity"),
            data.get("prior_screening"),
            data.get("prior_benign_breast_disease"),
            data.get("self_exam_irregularity"),
            "7",
            "9"
        ]], dtype=float)


    @staticmethod
    def interpret_risk(prob):
        if prob > 0.75:
            return {
                "label": "High Risk Detected",
                "guidelines": [
                    "Refer immediately to a breast / oncology specialist.",
                    "Arrange diagnostic tests(scan or biopsy).",
                    "Provide reassurance and support the patient."
                ]
            }
        elif prob > 0.5:
            return {
                "label": "Medium Rsk Detected",
                "guidelines": [
                    "Recommend further screening at a health facility.",
                    "Monitor symptoms closely and report any changes.",
                    "Schedule follow - up within 1–3 months."
                ]
            }
        else:
            return {
                "label": "Low Risk Detected",
                "guidelines": [
                    "Continue routine screening as recommended."
                    "Encourage monthly self - exams."
                    "Promote healthy lifestyle habits."
                ]
            }