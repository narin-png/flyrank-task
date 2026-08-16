from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import Response
from sqlmodel import SQLModel, Field, Session, select

from config import engine

app = FastAPI()


# --- Database model ---
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False


# --- Dependency: gives each request its own DB session ---
def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        existing = session.exec(select(Task)).first()
        if not existing:
            example_tasks = [
                Task(title="Learn FastAPI", done=False),
                Task(title="Build Task API", done=False),
                Task(title="Push project to GitHub", done=True),
            ]
            session.add_all(example_tasks)
            session.commit()


# --- Old in-memory array (still used by POST/PUT/DELETE for now) ---
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build Task API", "done": False},
    {"id": 3, "title": "Push project to GitHub", "done": True},
]


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.get("/", summary="API information")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}


# --- Stage 1: Read endpoints now use the database ---

@app.get("/tasks", summary="List all tasks")
def get_tasks(session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()


@app.get("/tasks/{task_id}", summary="Get task by ID")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    return task


# --- POST/PUT/DELETE still use the array — updated in Stage 2 and Stage 3 ---

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    new_task = Task(title=task.title, done=False)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, updated_task: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if updated_task.title is None and updated_task.done is None:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Request body cannot be empty"}
                )
            if updated_task.title is not None:
                if not updated_task.title.strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )
                task["title"] = updated_task.title
            if updated_task.done is not None:
                task["done"] = updated_task.done
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )