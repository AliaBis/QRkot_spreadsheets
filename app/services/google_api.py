from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings


#создать папаку с константами?
FORMAT = "%Y/%m/%d %H:%M:%S"
DATE_TIME = datetime.now().strftime(FORMAT)
TABLE = [
    ['Отчет на: ', DATE_TIME],
    ['Проекты по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
TABLE_BODY = dict(
    properties=dict(
        title=f'Отчет от {DATE_TIME}',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=100,
            columnCount=4,
        )
    ))]
)


async def spreadsheets_create(aiogoogle_object: Aiogoogle) -> str:
    """Создание таблицы"""
    service = await aiogoogle_object.discover('sheets', 'v4')
    response = await aiogoogle_object.as_service_account(
        service.spreadsheets.create(json=TABLE_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    print(spreadsheet_id)
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        aiogoogle_object: Aiogoogle
) -> None:
    """Предоставление прав доступа"""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await aiogoogle_object.discover('drive', 'v3')
    await aiogoogle_object.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        aiogoogle_object: Aiogoogle
) -> None:
    """Запись инфы из базы данных в документ с таблицами"""
    service = await aiogoogle_object.discover('sheets', 'v4')
    table_values = TABLE
    for project in projects:
        print(project, type(project))
        new_row = [
            str(project['name']),
            str(timedelta(project['_no_label'])),
            str(project['description'])
        ]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    try:
        await aiogoogle_object.as_service_account(
            service.spreadsheets.values.update(
                spreadsheetId=spreadsheet_id,
                range='A1:D100',
                valueInputOption='USER_ENTERED',
                json=update_body
            )
        )
    except ValueError:
        print('Проверь входящие данные')
