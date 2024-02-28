import logging
from fastapi import FastAPI
from pydantic import BaseModel
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
#uvicorn app:app --reload

class Task(BaseModel):
    text: str

@app.get("/tasks")
async def read_all():
    with open("tasks.json", "r") as file:
        data = json.load(file)
        file.close()
        logger.info(f'Отработал get запрос. Выведен весь список задач')
    ndata = {}
    for k, v in data.items():
        if v != 'Deleted':
            ndata[k] = data[k]
    return ndata

@app.get("/tasks/{id}")
async def read_id(id:str):
    with open("tasks.json", "r") as file:
        data = json.load(file)
        file.close()
    task:dict = data[id]
    logger.info(f'Отработал get запрос. Выведена задача {id}')
    return task

#curl -X 'POST' 'http://127.0.0.1:8000/tasks/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"text": "New task"}'
@app.post("/tasks/")
async def new_task(task:Task):
    with open("tasks.json", "r") as file:
        data = json.load(file)
        file.close()
    id = 0
    for k in data.keys():
        id = k
    data[str(int(id)+1)] = task.text
    
    with open("tasks.json", "w") as file:
        json.dump(data, file)
        file.close()
    logger.info(f'Отработал post запрос. Добавлена задача: {data[id +1]}')


#curl -X 'PUT' 'http://127.0.0.1:8000/tasks/4' -H 'accept: application/json' -H 'Content-Type: application/json' -d'{"text": "Done"}'
@app.put("/tasks/{id}")
async def update_task(id:str, task:Task):
    with open("tasks.json", "r") as file:
        data = json.load(file)
        file.close()
    for k in data.keys():
        if k == id:
            data[k] = task.text

    with open("tasks.json", "w") as file:
        json.dump(data, file)
        file.close()
    logger.info(f'Отработал put запрос. Задача {id} имеет статус \"Выполнена\"')
    

#curl -X 'DELETE' 'http://127.0.0.1:8000/tasks/4' -H 'accept: application/json'
@app.delete("/tasks/{id}")
async def delete_task(id:str):
    with open("tasks.json", "r") as file:
        data = json.load(file)
        file.close()

    for k in data.keys():
        if k == id:
            data[k]='Deleted'
            break

    with open("tasks.json", "w") as file:
        json.dump(data, file)
        file.close()
    logger.info(f'Отработал delete запрос. Задача {id} удалена')