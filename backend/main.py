from contextlib import asynccontextmanager
from backend.models.engine import Base
from backend.models import database
from backend.API import routes
from fastapi import FastAPI



@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield

app = FastAPI(title="API_Sistema_de_contas", lifespan=lifespan)
app.include_router(routes.router)