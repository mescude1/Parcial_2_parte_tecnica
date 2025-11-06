from sqlalchemy.orm import Session
from persistence.task_repository import TaskRepository
from persistence.models import Task


class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)

    def get_all_tasks(self):
        return self.repo.get_all()

    def create_task(self, name: str):
        # Example: business rule — prevent duplicates
        existing = [task for task in self.repo.get_all() if task.name == name]
        if existing:
            raise ValueError(f"Task with name '{name}' already exists.")
        return self.repo.create_task(name)

    def update_task_status(self, task_id: int, status: str):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        self.repo.update_task_status(task, status)
        return task

    def delete_task(self, task_id: int):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        self.repo.delete_task(task)
        return task