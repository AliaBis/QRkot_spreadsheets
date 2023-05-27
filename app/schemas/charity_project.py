from datetime import datetime

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectCreate(BaseModel):
    """Получение данных."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(CharityProjectCreate):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: PositiveInt = Field(None)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    """Возвращение объекта."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime = Field(None)

    class Config:
        orm_mode = True


class CharityProjectGoogle(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    time: int
    description: str = Field(..., min_length=1)

    class Config:
        orm_mode = True