import asyncio
from typing import Union

from fastapi import BackgroundTasks
from pydantic import BaseModel, validator, model_validator

from app.loader import app

tasks_list = []


class ItemParam(BaseModel):
    x: int
    y: int
    oper: str

    @validator('oper')
    def check_oper(cls, value):
        if value not in ['+', '-', '/', '*']:
            raise ValueError('Оператор должен быть "+", "-", "/", "*"')
        return value

    @model_validator(mode='after')
    def check_y(cls, values):
        if values.oper == '/' and values.y == 0:
            raise ValueError('Деление на 0 невозможно')
        return values


class TaskParam(BaseModel):
    task_id: int

    @validator('task_id')
    def check_oper(cls, value):
        if value - 1 >= len(tasks_list):
            raise ValueError('ID данной задачи отсутствует')
        return value


async def get_param(x, y, oper):
    response = {}
    exec(f'result = {x}{oper}{y}', response)
    return response['result']


@app.get('/item/')
async def create_task(x: Union[int], y: Union[int], oper: Union[str], tasks: BackgroundTasks):
    ItemParam(x=x, y=y, oper=oper)
    task_id = len(tasks_list) + 1
    task = asyncio.create_task(get_param(x, y, oper))
    task.name = f'Task {task_id}'
    tasks_list.append(task)
    print(tasks_list)
    return task_id


@app.get('/task/')
async def task_result(task_id):
    TaskParam(task_id=task_id)
    task = tasks_list[int(task_id) - 1]
    result = await task
    return result


@app.get('/tasks_status_list/')
async def tasks_status_list():
    result = {}
    for i, task in enumerate(tasks_list):
        result[f'task_id: {i}'] = {"name": f"{task.name}", "status": {"done" if task.done() else "processing"}}
    return result
