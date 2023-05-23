# QRkot_spreadseets

## Фонд собирает пожертвования на поддержку котиков.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается. Следующие пожертвования поступают уже в новый проект.

* Любой посетитель сайта (в том числе неавторизованный) может посмотреть список всех проектов.
* Суперпользователь может: 
 * * создавать проекты,
 * * удалять проекты, в которые не было внесено средств,
 * * изменять название и описание существующего проекта, устанавливать для него новую требуемую сумму (но не меньше уже внесённой).
* Никто не может менять через API размер внесённых средств, удалять или модифицировать закрытые проекты, изменять даты создания и закрытия проектов.
________________________
## Используемый стек:
```
Python, FastAPI, SQLAlchemy, Asyncio, 
Google Cloud Platform, Google Sheets API, Google Drive API
```
__________________________
## Как запустить проект:
 Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/AliaBis/QRkot_spreadsheets
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
Обновить и установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции,чтобы создать базу данных SQLite:
```
alembic upgrade head
```
Запустить проект локально:
```
uvicorn app.main:app --reload
```

После запуска проект доступен по адресам:

* http://127.0.0.1:8000 - API
* http://127.0.0.1:8000/docs - документация Swagger
* http://127.0.0.1:8000/redoc - документация ReDoc

Эндпоинты:

Регистрация и аутентификация:
* /auth/register - регистрация нового пользователя
* /auth/jwt/login - аутентификация пользователя (получение jwt-токена)
* /auth/jwt/logout - выход

Пользователи:
* /users/me - получение и изменение данных зарегистрированного пользователя
* /users/{id} - получение и изменение данных пользователя по id

Благотворительные проекты:
* /charity_project/ - получение списка всех проектов и создание нового
* /charity_project/{project_id} - изменение и удаление существующего проекта

Пожертвования:
* /donation/ - получение списка всех пожертвований и создание пожертвования
* /donation/my - получение списка всех пожертвований зарегистрированного пользователя

При первом запуске приложения создается суперюзер с рег.данными из .env


______________________
Автор:

Алия Бисенгалиева