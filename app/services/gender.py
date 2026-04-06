from app.repositories import GenderRepository

class GenderService:
    def __init__(self, repo: GenderRepository):
        self.repo = repo

    async def index(self):
        return await self.repo.index()