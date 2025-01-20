from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from models.task import Task
from models.user import User
from schemas import CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    """
    Возвращает все задачи.
    """
    tasks = db.execute(select(Task)).scalars().all()
    if tasks == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Задач нет')
    else:
        return tasks


@router.get('/{task_id}')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    """
    Возвращает конктерную задачу по id.
    """

    task = db.scalar(select(Task).where(Task.id == int(task_id)))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Задача под данным id не найдена')
    else:
        return task


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask):
    """
    Создаем новой задачи
    """
    # проверяем есть ли такой пользователь:
    user = db.scalar(select(User).where(User.id == create_task.user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь с указанным id не существует')
    else:
        # проверяем есть ли такая задача у данного пользователя
        slug = create_task.title + str(create_task.user_id)
        tasks = db.scalar(
            select(Task).where(Task.user_id == create_task.user_id).where(Task.slug == slugify(slug)))
        if tasks is None:
            db.execute(insert(Task).values(
                title=create_task.title,
                content=create_task.content,
                priority=create_task.priority,
                slug=slugify(slug),
                user_id=create_task.user_id))
            db.commit()
            return {
                'status_code': status.HTTP_201_CREATED,
                'transaction': 'Successful'
            }
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='У данного пользователя уже есть такая задача')


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    """
    Обновляет данные задачи если такая задача
    """
    'Проверяем, есть ли такая задача'
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Задача под данным id не найдена')
    else:
        db.execute(update(Task).where(Task.id == task_id).values(
            title=update_task.title,
            content=update_task.content,
            priority=update_task.priority))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful!'
        }


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    """
    Удаляет задачу если такая задача
    """
    # Проверяем, есть ли такая задача'
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Задача под данным id не найдена')
    else:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deleted is successful!'}
