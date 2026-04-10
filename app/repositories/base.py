from typing import Type, Generic, TypeVar, Optional, List

from sqlalchemy import Select, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
# Add this import at the top of base.py
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException


ModelType = TypeVar("ModelType", bound=DeclarativeBase)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, data: dict) -> ModelType:
        try:
            obj = self.model(**data)
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return  { "message": "Record created successfully" }

        except IntegrityError as e:
            await self.db.rollback()

            if "patients_name_key" in str(e):
                raise HTTPException(409, f"Patient with name already exists!")
            else:
                raise HTTPException(400, "Database integrity error occurred")



    async def update(self, obj_id: int, data: dict) -> Optional[ModelType]:
        try:
            obj = await self.db.get(self.model, obj_id)

            if not obj:
                return None

            for key, value in data.items():
                setattr(obj, key, value)

            await self.db.commit()
            await self.db.refresh(obj)

            return { "message": "Record updated successfully" }
        except IntegrityError as e:
            await self.db.rollback()

            if "patients_name_key" in str(e):
                raise HTTPException(409, f"Patient with name already exists!")
            else:
                raise HTTPException(400, "Database integrity error occurred")


    async def delete(self, obj_id: int) -> bool:
        obj = await self.db.get(self.model, obj_id)

        if not obj:
            return False

        await self.db.delete(obj)
        await self.db.commit()
        return True


    async def get(self, obj_id: int) -> Optional[ModelType]:
        return await self.db.get(self.model, obj_id)


    async def get_by(
        self,
        options: Optional[List] = None,
        include_inactive: bool = False
    ) -> Optional[ModelType]:
        stmt: Select = select(self.model)

        # Optional "active" filter
        if hasattr(self.model, "active") and not include_inactive:
            stmt = stmt.where(self.model.active == True)

        # Apply loading options like joinedload or selectinload
        if options:
            for opt in options:
                stmt = stmt.options(opt)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()