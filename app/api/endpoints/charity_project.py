from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_charity_project_edit, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.process_investing import (close_donation,
                                            process_investments)

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создание документа только для суперпользователей."""

    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await process_investments(session)
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        json_data_user: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Обновление для суперпользователей."""

    full_amount = json_data_user.full_amount
    existing_project = await check_charity_project_edit(
        project_id, session, full_amount=full_amount
    )
    # if json_data_user.name is not None:
    await check_name_duplicate(json_data_user.name, session)
    if full_amount == existing_project.invested_amount:
        existing_project.full_amount = full_amount
        close_donation(existing_project)
    updated_project = await charity_project_crud.update(
        existing_project, json_data_user, session
    )
    return updated_project
    

@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователей."""

    existing_project = await check_charity_project_edit(
        project_id, session, delete=True
    )
    deleted_project = await charity_project_crud.remove(
        existing_project, session
    )

    return deleted_project
