from src.domain.entities.avatar import Avatar, DBAvatar


class AvatarService:
    @staticmethod
    def create_avatar(image_url: str) -> Avatar:
        return Avatar(image_url=image_url)

    @staticmethod
    def update_avatar(existing_avatar: DBAvatar, avatar: Avatar) -> DBAvatar:
        return DBAvatar(
            id=existing_avatar.id,
            image_url=avatar.image_url if avatar.image_url else existing_avatar.image_url
        )
