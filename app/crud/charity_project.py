from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject

from .base import CRUDBase


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self, session: AsyncSession) -> list[dict]:
        """Oтсортирует список со всеми закрытыми проектами."""
        projects = await session.execute(
            select(
                CharityProject.name, CharityProject.close_date,
                CharityProject.create_date,
                CharityProject.description).where(
                    CharityProject.fully_invested))
        result = []
        for obj in projects:
            result.append({
                'name': obj.name,
                'delta': obj.close_date - obj.create_date,
                'description': obj.description})
        return sorted(result, key=lambda x: x['delta'])


charity_project_crud = CRUDCharityProject(CharityProject)
