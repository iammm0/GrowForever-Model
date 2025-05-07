from fastapi import FastAPI

from routers import tests, expand
from utils.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(tests.router)
app.include_router(expand.router)