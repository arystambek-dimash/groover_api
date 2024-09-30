import os
from dataclasses import dataclass
from os import environ as env
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MEDIA_DIR = BASE_DIR / 'media_files'
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class DBSettings:
    db_name: str
    host: str
    password: str
    user: str
    port: int

    @property
    def db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass
class CORSSettings:
    frontend_url: str


@dataclass
class JWTSettings:
    jwt_secret_key: str


@dataclass
class Settings:
    db: DBSettings
    cors: CORSSettings
    jwt: JWTSettings
    backend_url: str


def load_settings() -> Settings:
    """Get app settings"""
    db = DBSettings(
        db_name=env["POSTGRES_DB"],
        host=env["POSTGRES_HOST"],
        password=env["POSTGRES_PASSWORD"],
        user=env["POSTGRES_USER"],
        port=int(env["POSTGRES_PORT"]),
    )

    cors = CORSSettings(frontend_url=env.get("FRONTEND_URL", "localhost:3000"))
    jwt = JWTSettings(jwt_secret_key=env["JWT_SECRET_KEY"])
    backend_url = env.get("BACKEND_URL", "http://localhost:8000")
    return Settings(
        db=db,
        cors=cors,
        jwt=jwt,
        backend_url=backend_url,
    )


settings = load_settings()
