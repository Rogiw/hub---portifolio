#python -m uvicorn apps.main:app --host 0.0.0.0 --port 8000
from fastapi import FastAPI
from apps.portfolio.routes import chem, dev
from apps.api import health
#from apps.marketplace.routes import marketplace
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="ComputHub API",
    description="ComputHub is a platform that provides access to various computational resources and services. It allows users to run computational tasks, manage resources, and access data through a unified API.",
    version="0.1.0",
    contact={
        "name": "Wigor Rodrigues"})


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://seu-site.vercel.app",
        "https://wigorrodrigues.com.br",
        "https://www.wigorrodrigues.com.br",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""msg do que será enviado quando acessar a raiz da API"""
@app.get("/")
def root():
    return {"message": "Welcome to the ComputHub API!"}

app.include_router(chem.router)
app.include_router(dev.router)