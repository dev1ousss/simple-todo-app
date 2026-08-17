from contextlib import asynccontextmanager

from app.datasource.database.session import engine
from app.datasource.models.base import Base
from app.web.routers.categories import router as category_router
from app.web.routers.tasks import router as task_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)

app.include_router(router=task_router)
app.include_router(router=category_router)
