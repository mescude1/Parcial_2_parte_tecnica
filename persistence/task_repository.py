from sqlalchemy.orm import Session
from persistence.models import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Task).all()

    def get_by_id(self, item_id: int):
        return self.db.query(Task).filter(Task.id == item_id).first()

    def create_task(self, name: str):
        task = Task(name=name)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task_status(self, task: Task, status: str):
        task.status = status
        self.db.commit()
        self.db.refresh(task)

    def delete_task(self, task: Task):
        self.db.delete(task)
        self.db.commit()