# Task API

A simple CRUD API built with FastAPI. The project manages tasks using in-memory storage (no database).

## Run the project

```bash
python -m uvicorn main:app --reload
```

Open the API:

* API: http://127.0.0.1:8000
* Swagger UI: http://127.0.0.1:8000/docs

## Endpoints

| Method | Endpoint         | Description                                                                                                                                 |
| ------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| GET    | /                | Returns API information including name, version and available endpoints.                                                                    |
| GET    | /health          | Checks whether the API is running and returns the server status.                                                                            |
| GET    | /tasks           | Returns the complete list of tasks.                                                                                                         |
| GET    | /tasks/{task_id} | Returns a single task by its ID. Returns **404** if the task does not exist.                                                                |
| POST   | /tasks           | Creates a new task. Assigns a new ID, sets **done = false**, and returns **201 Created**. Returns **400** if the title is missing or empty. |
| PUT    | /tasks/{task_id} | Updates a task's title and/or completion status. Returns **404** if the task is not found and **400** for invalid input.                    |
| DELETE | /tasks/{task_id} | Deletes a task and returns **204 No Content**. Returns **404** if the task does not exist.                                                  |

## Example curl

```bash
curl.exe -i http://127.0.0.1:8000/tasks
```

## Swagger UI Screenshots

### Get All Tasks

![Get All Tasks](images/getAll.png)

### Get Task by ID (Success)

![Get Task by ID Success](images/getById-success.png)

### Get Task by ID (404 Error)

![Get Task by ID Error](images/getById-error.png)

### Create Task (Success)

![Create Task Success](images/post-success.png)

### Create Task (Validation Error)

![Create Task Error](images/post-error.png)

### Update Task (Success)

![Update Task Success](images/put success.png)

### Update Task (Empty Title)

![Update Task Empty Title](images/put-blank.png)

### Update Task (Unknown ID)

![Update Task Unknown ID](images/put-unknownid.png)

### Delete Task (Success)

![Delete Task Success](images/delete-success.png)

### Delete Task (Unknown ID)

![Delete Task Error](images/delete-error.png)
