from app.repositories import DocumentCategoryRepository

class DocumentCategoryService:
    def __init__(self, repo: DocumentCategoryRepository):
        self.repo = repo

    async def index(self):
        return await self.repo.index()