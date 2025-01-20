# Аннотации, Модели БД и Pydantic.
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
# Функция создания slug-строки
from slugify import slugify
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Сессия БД
from sqlalchemy.orm import Session

# Функция подключения к БД
from backend.db_depends import get_db
from models.user import User
from schemas import CreateUser, UpdateUser

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_user(db: Annotated[Session, Depends(get_db)]):
    """
    Возвращает всех пользователей.
    """
    users = db.execute(select(User)).scalars().all()
    if users == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователей нет')
    else:
        return users


@router.get('/{user_id}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    """
    Возвращает конктерного пользователя по id.
    """

    user = db.scalar(select(User).where(User.id == int(user_id)))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь под данным id не найден')
    else:
        return user


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    """
    Создаем нового пользователя
    """
    # проверяем есть ли такой пользователь:
    user = db.scalar(select(User).where(User.username == create_user.username))
    if user is None:
        db.execute(insert(User).values(
            username=create_user.username,
            firstname=create_user.firstname,
            lastname=create_user.lastname,
            age=create_user.age,
            slag=slugify(create_user.username)))
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь с таким username уже существует')


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    """
    Обновляет данные пользователя если такой пользователь
    """
    'Проверяем, есть ли такой пользователь'
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь под данным id не найден')
    else:
        db.execute(update(User).where(User.id == user_id).values(
            firstname=update_user.firstname,
            lastname=update_user.lastname,
            age=update_user.age))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'
        }


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    """
    Удаляет пользователя если такой пользователь есть
    """
    'Проверяем, есть ли такой пользователь'
    user = db.scalar(select(User).where(User.id == int(user_id)))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь под данным id не найден')
    else:
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User deleted is successful!'}
