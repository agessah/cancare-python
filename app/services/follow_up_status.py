from app.repositories import FollowUpStatusRepository

class FollowUpStatusService:
    def __init__(self, repo: FollowUpStatusRepository):
        self.repo = repo

    async def index(self):
        return await self.repo.index()