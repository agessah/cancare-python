from app.repositories import LevelRepository

class LevelService:
    def __init__(self, repo: LevelRepository):
        self.repo = repo

    async def index(self):
        return await self.repo.index()