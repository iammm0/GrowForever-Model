from fastapi import FastAPI

from api.routers import users
from api.routers import tests, gpts, nodes
from utils.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(nodes.router)
app.include_router(gpts.router)
app.include_router(tests.router)