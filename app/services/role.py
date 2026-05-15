from typing import List

from app.repositories import RoleRepository, PermissionRepository
from fastapi import HTTPException


class RoleService:
    def __init__(self, repo: RoleRepository, perm_repo: PermissionRepository):
        self.repo = repo
        self.perm_repo = perm_repo

    async def show(self, resource_id: int):
        resource = await self.repo.get(resource_id)

        if not resource:
            raise HTTPException(404, "Role not found")

        return { "data": resource }

    async def assign_permissions(self, role_id: int, permission_ids: List[int]):
        role = await self.repo.get(role_id)

        if not role:
            raise HTTPException(404, "Role not found")

        permissions = await self.perm_repo.get_permissions(permission_ids)
        if not permissions:
            raise HTTPException(404, "No matching permissions found")

        return await self.repo.sync_permissions(role, permissions)
