from typing import Optional
from src.domain.entities.style import Style, DBStyle


class StyleService:
    @staticmethod
    async def create_style(name: str, image_url: str) -> Style:
        return Style(name=name, image_url=image_url)

    @staticmethod
    async def update_style(db_style: DBStyle, name: Optional[str] = None, image_url: Optional[str] = None) -> DBStyle:
        if name:
            db_style.name = name
        if image_url:
            db_style.image_url = image_url
        return db_style
