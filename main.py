from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import Response
from sqlmodel import SQLModel, Field, Session, select

from config import engine

app = FastAPI()


# --- Database model (Stage 0) ---
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    done: bool = False


@app.on_event("startup")
def on_startup():
    # Create the tasks table if it doesn't already exist
    SQLModel.metadata.create_all(engine)

    # Insert example tasks only if the table is empty
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


# --- Old in-memory array (still used by endpoints below for now, will be removed in Stage 1) ---
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build Task API",
        "done": False
    },
    {
        "id": 3,
        "title": "Push project to GitHub",
        "done": True
    }
]

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.get("/",
    summary="API information")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health",
    summary="Health check")
def health():
    return {
        "status": "ok"
    }

@app.get("/tasks",
    summary="List all tasks"
)
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}",
    summary="Get task by ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {task_id} not found"
        }
    )


@app.post("/tasks", status_code=201,
    summary="Create a new task")
def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={
                "error": "Title cannot be empty"
            }
        )

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{task_id}",
    summary="Update a task")
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


@app.delete("/tasks/{task_id}", status_code=204,
    summary="Delete a task")
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )