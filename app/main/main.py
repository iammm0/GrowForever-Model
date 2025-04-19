from fastapi import FastAPI

from app.api.routers import nodes
from app.api.routers import tests, gpts, users
from app.utils.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(nodes.router)
app.include_router(gpts.router)
app.include_router(tests.router)