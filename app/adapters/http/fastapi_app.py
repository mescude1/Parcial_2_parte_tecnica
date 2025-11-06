from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from persistence import models
from persistence.database_setup import engine, get_db
from persistence.schemas import TaskCreate, TaskStatusUpdate, TaskResponse
from services.task_service import TaskService

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get task service
def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)

@app.get("/tasks/", response_model=List[TaskResponse])
def get_all_tasks(task_service: TaskService = Depends(get_task_service)):
    return task_service.get_all_tasks()

@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, task_service: TaskService = Depends(get_task_service)):
    try:
        return task_service.create_task(task.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/tasks/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, status_update: TaskStatusUpdate, task_service: TaskService = Depends(get_task_service)):
    try:
        return task_service.update_task_status(task_id, status_update.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    try:
        return task_service.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))