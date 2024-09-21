from dataclasses import dataclass
from os import environ as env
from dotenv import load_dotenv

load_dotenv()


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


def load_settings() -> Settings:
    """Get app settings"""
    db = DBSettings(
        db_name=env["POSTGRES_DB"],
        host=env["POSTGRES_HOST"],
        password=env["POSTGRES_PASSWORD"],
        user=env["POSTGRES_USER"],
        port=int(env["POSTGRES_PORT"]),
    )

    cors = CORSSettings(frontend_url=env.get("FRONTEND", "localhost:3000"))
    jwt = JWTSettings(jwt_secret_key=env["JWT_SECRET_KEY"])
    return Settings(
        db=db,
        cors=cors,
        jwt=jwt
    )


settings = load_settings()
