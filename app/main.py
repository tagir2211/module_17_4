from fastapi import FastAPI

from routers import task, user

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)


@app.get("/")
def read_root():
    return {"message": "Welcome to Taskmanager"}



app.include_router(user.router)
app.include_router(task.router)


