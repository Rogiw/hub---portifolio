#uvicorn main: apps.main:app --host 0.0.0.0 --port 8000
from fastapi import FastAPI
from apps.lab.routes.projects import router as projects_router
from apps.api import health
#from apps.marketplace.routes import marketplace


app = FastAPI(
    title="ComputHub API",
    description="ComputHub is a platform that provides access to various computational resources and services. It allows users to run computational tasks, manage resources, and access data through a unified API.",
    version="0.1.0",
    contact={
        "name": "Wigor Rodrigues"})

"""msg do que será enviado quando acessar a raiz da API"""

@app.get("/")
def root():
    return {"message": "Welcome to the ComputHub API!"}

app.include_router(projects_router)