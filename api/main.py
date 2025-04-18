from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="Jueguitos.AI")

app.include_router(router)
