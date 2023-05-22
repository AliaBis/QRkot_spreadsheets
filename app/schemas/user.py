from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема базовых полей модели пользователя."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема создания пользователя."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема обновления объекта пользователя."""
    pass
