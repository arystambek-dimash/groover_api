import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.adapters.database.session import get_async_sessionmaker, get_engine
from src.main.config import settings
from src.main.ioc import IoC
from src.presentation.api.endpoints import include_routers, include_exception_handlers
from src.presentation.interactor_factory import InteractorFactory

app = FastAPI(
    docs_url='/api/docs',
    redoc_url='/api/redoc',
)

origins = [
    settings.cors.frontend_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

include_exception_handlers(app)


@app.on_event("startup")
async def on_startup() -> None:
    engine_factory = get_engine(settings.db)
    engine = await anext(engine_factory)
    session_factory: async_sessionmaker[AsyncSession] = await get_async_sessionmaker(engine)
    ioc: InteractorFactory = IoC(session_factory=session_factory)

    app.dependency_overrides = {InteractorFactory: lambda: ioc}
    include_routers(app)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", workers=1, port=8000)
