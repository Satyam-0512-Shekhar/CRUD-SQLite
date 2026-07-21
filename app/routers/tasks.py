from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Task, TaskCreate, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/", response_model=list[Task])
def get_tasks(session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    db_task = Task(title=task.title, done=False)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    updated_task: TaskUpdate,
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if not updated_task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    task.title = updated_task.title
    task.done = updated_task.done

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()