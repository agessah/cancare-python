import mimetypes
import os
import uuid
from pathlib import Path

import aiofiles
from fastapi.responses import FileResponse

from app.core.config import Settings
from app.repositories import DocumentRepository
from fastapi import UploadFile, File, HTTPException, Depends, Request


class DocumentService:
    def __init__(self, settings: Settings, repo: DocumentRepository):
        self.repo = repo
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)


    async def create(
        self,
        file: UploadFile = File(...),
        data: dict = Depends()
    ):
        try:
            original_name = file.filename
            if not original_name:
                raise HTTPException(400, "File must have a filename")

            ext = Path(original_name).suffix
            if not ext:
                raise HTTPException(400, "Invalid file extension!")

            filename = f"{uuid.uuid4()}{ext}"

            file_path = os.path.join(self.upload_dir, filename)

            async with aiofiles.open(file_path, "wb") as out_file:
                content = await file.read()
                await out_file.write(content)

            data["path"] = file_path

        except Exception:
            raise HTTPException(400, "File must have a filename")

        return await self.repo.create(data)


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
            raise HTTPException(status_code=404, detail="Document not found")

        return resource


    async def download(self, resource_id: int, download: bool):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(404, "File not found")

        file_path = Path(resource.path).resolve()

        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(404, "File not found")

        # Detect content type
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"

        # Set disposition
        disposition = "attachment" if download else "inline"

        headers = {
            "Content-Disposition": f'{disposition}; filename="{resource.name}"'
        }

        return FileResponse(
            path=file_path,
            media_type=content_type,
            headers=headers
        )