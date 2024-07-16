import asyncio
from typing import Union

from fastapi import BackgroundTasks

from app.loader import app

tasks_list = []


def check_parametrs(x, y, oper):
    try:
        x, y = map(int, [x, y])
        if y == 0:
            raise ZeroDivisionError('Деление на ноль невозможно.')
    except ValueError:
        raise ValueError('Неверные параметры. x и y должны быть целыми числами.')

    if oper not in ['+', '-', '*', '/']:
        raise ValueError('Неверная операция')


async def get_param(x, y, oper):
    response = {}
    exec(f'result = {x}{oper}{y}', response)
    return response['result']


@app.get('/item/')
async def create_task(x: Union[int], y: Union[int], oper: Union[str], tasks: BackgroundTasks):
    check_parametrs(x, y, oper)
    task_id = len(tasks_list) + 1
    task = asyncio.create_task(get_param(x, y, oper))
    task.name = f'Task {task_id}'
    tasks_list.append(task)
    print(tasks_list)
    return task_id


@app.get('/task/')
async def task_result(task_id):
    task = tasks_list[int(task_id) - 1]
    result = await task
    return result


@app.get('/tasks_status_list/')
async def tasks_status_list():
    result = []
    for task in tasks_list:
        result.append(f"Name: '{task.name}'  status: {'Done' if task.done() else 'Processing'}")
    return result
