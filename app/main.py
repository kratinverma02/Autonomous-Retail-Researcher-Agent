from fastapi import FastAPI
from .controller import router

app = FastAPI(title="Autonomous Retail Researcher Agent")

app.include_router(router)
