from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes import api_router
from app.scheduler import scheduler


@asynccontextmanager
async def app_lifespan(fastapi: FastAPI):
    # on-startup
    scheduler.start()
    scheduler.add_calculator_task()

    yield
    # on-shutdown
    scheduler.shutdown()

app = FastAPI(
    lifespan=app_lifespan,
    # TODO: An API-KEY is needed here to secure the access to the API
)
app.include_router(api_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=3333, log_level='info')
