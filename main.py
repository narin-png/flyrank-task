from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import Response

app = FastAPI()


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

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
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


@app.post("/tasks", status_code=201)
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

@app.put("/tasks/{task_id}")
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


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )