from app.repositories import MediaTypeRepository

class MediaTypeService:
    def __init__(self, repo: MediaTypeRepository):
        self.repo = repo

    async def index(self):
        return await self.repo.index()