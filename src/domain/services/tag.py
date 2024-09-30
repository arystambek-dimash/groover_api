from dataclasses import asdict
from typing import TypeVar, List

from src.adapters.database.models import TagOrm
from src.domain.entities.tag import Tag, DBTag

T = TypeVar('T')


class TagService:
    @staticmethod
    def create_tag_entity(dto: T) -> Tag:
        if isinstance(dto, str):
            return Tag(
                name=dto
            )
        return Tag(
            name=dto.name
        )

    @staticmethod
    def update_tag(existing_tag: DBTag, dto: Tag) -> DBTag:
        if dto.name:
            existing_tag.name = dto.name
        return existing_tag

    async def add_tags(self, tag_names: List[str]) -> List[TagOrm]:
        db_tags = []
        for name in tag_names:
            tag_entity = self.create_tag_entity(name)
            db_tags.append(tag_entity)
        return db_tags
