from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.db.session import init_db
from api.events import router as event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup
    print("123")
    init_db()
    yield
    # clean up


app = FastAPI(lifespan=lifespan)
app.include_router(event_router, prefix="/api/events")


@app.get("/")
def hello_index():
    return {
        "message": "hello!"
    }


@app.get("/healthz")
def get_status():
    return {
        "status": "ok"
    }
