from fastapi import FastAPI
from backend.db import Base,engine
from routers import task, user

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)


@app.get("/")
def read_root():
    return {"message": "Welcome to Taskmanager"}



app.include_router(user.router)
app.include_router(task.router)

Base.metadata.create_all(bind=engine)

