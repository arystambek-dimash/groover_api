from datetime import datetime, timedelta
from typing import Optional

from src.application.interfaces.uow import UoW
from src.application.interfaces.repository import UserRepository, AvatarRepository
from src.application.interfaces.repository import RoleRepository
from src.domain.exceptions.base import NotFound

from src.domain.services.user import UserService
from src.application.user.jwt import JWTService

from src.domain.entities.user import User, DBUser
from src.domain.entities.staff import Staff
from src.domain.entities.client import Client

from src.domain.value_objects.user import UserEmail

from src.application.user.dto import (
    CreateUserDTO,
    CreateStaffDTO,
    ResponseUserDTO,
    UserLoginDTO,
    TokenDTO,
    UpdateUserDTO,
    PayloadDTO,
)

from src.domain.exceptions.jwt import JWTDecodeError
from src.domain.exceptions.user import (
    InvalidEmailError,
    UserIsNotExistsError,
    UserAlreadyExistsError,
    IsNotAdminError,
    InvalidPasswordError,
)


class UserInteractor:
    def __init__(
            self,
            user_repository: UserRepository,
            staff_repository: RoleRepository,
            client_repository: RoleRepository,
            avatar_repository: AvatarRepository,
            uow: UoW,
            user_service: UserService,
            jwt_service: JWTService,
    ):
        self._user_repository = user_repository
        self._staff_repository = staff_repository
        self._client_repository = client_repository
        self._avatar_repository = avatar_repository
        self._uow = uow
        self._user_service = user_service
        self._jwt_service = jwt_service
        self._REFRESH_TOKEN_EXPIRE_DAYS = 30
        self._ACCESS_TOKEN_EXPIRE_MINUTES = 3

    async def sign_up_client(self, data: CreateUserDTO) -> ResponseUserDTO:
        await self._ensure_user_does_not_exist(data.email)
        user: User = self._user_service.create_user(data.email, data.password)
        db_user = await self._user_repository.add(user)
        client = Client(user=db_user)
        await self._client_repository.add(client)
        await self._uow.commit()
        return self._create_response_user_dto(db_user, None)

    async def sign_up_staff(self, data: CreateStaffDTO) -> ResponseUserDTO:
        await self._ensure_user_does_not_exist(data.email)
        user: User = self._user_service.create_user(data.email, data.password)
        db_user = await self._user_repository.add(user)
        staff = Staff(user=db_user, role=data.role)
        await self._staff_repository.add(staff)
        await self._uow.commit()
        return self._create_response_user_dto(db_user, staff)

    async def sign_in(self, data: UserLoginDTO, staff_auth=False) -> TokenDTO:
        user = await self._get_user_by_email(data.email)
        if not self._user_service.verify_password(data.password, user.password.value):
            raise InvalidPasswordError("Invalid password.")

        if staff_auth:
            staff = await self._staff_repository.get_by_user_id(user_id=user.id)
            if not staff or not staff.role.value:
                raise IsNotAdminError("No such staff account.")

        tokens = self._create_tokens(user.id)
        staff_member = await self._staff_repository.get_by_user_id(user.id)

        return TokenDTO(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            role=staff_member.role.value if staff_member else 'CLIENT',
        )

    async def refresh_token(self, refresh_token: str) -> TokenDTO:
        try:
            payload = self._jwt_service.decode(refresh_token)
        except Exception as e:
            raise JWTDecodeError("Invalid refresh token.") from e

        user_id = payload.sub
        if not user_id:
            raise JWTDecodeError("Invalid refresh token payload.")

        user = await self._user_repository.get(user_id)
        if not user:
            raise UserIsNotExistsError("User does not exist.")

        new_access_token = self._create_access_token(user.id)
        return TokenDTO(
            access_token=new_access_token,
            refresh_token=refresh_token,
        )

    async def update_profile(self, user_id: int, data: UpdateUserDTO) -> ResponseUserDTO:
        user = await self._user_repository.get(user_id)
        if not user:
            raise UserIsNotExistsError("User does not exist.")
        if data.avatar_id:
            avatar = await self._avatar_repository.get(data.avatar_id)
            if not avatar:
                raise NotFound('Avatar does not exist.')
        user: User = self._user_service.update_user(
            user=user,
            password=data.password,
            username=data.username,
            avatar_id=data.avatar_id
        )
        await self._user_repository.update(user)
        await self._uow.commit()
        staff_member = await self._staff_repository.get_by_user_id(user_id)
        new_user = await self._user_repository.get(user_id)
        return self._create_response_user_dto(new_user, staff_member)

    async def get_profile(self, user_id: int) -> ResponseUserDTO:
        user = await self._user_repository.get(user_id)
        if not user:
            raise UserIsNotExistsError("User does not exist.")

        staff_member = await self._staff_repository.get_by_user_id(user_id)
        return self._create_response_user_dto(user, staff_member)

    async def _ensure_user_does_not_exist(self, email: str):
        try:
            email_vo = UserEmail(email)
        except ValueError as e:
            raise InvalidEmailError(str(e))

        if await self._user_repository.get_by_email(email_vo.value):
            raise UserAlreadyExistsError(f"User with email {email} already exists.")

    async def _get_user_by_email(self, email: str) -> DBUser:
        try:
            email_vo = UserEmail(email)
        except ValueError as e:
            raise InvalidEmailError(str(e))

        user = await self._user_repository.get_by_email(email_vo.value)
        if not user:
            raise UserIsNotExistsError("User does not exist.")
        return user

    def _create_token(self, user_id: int, expires_delta: timedelta) -> str:
        expire = datetime.utcnow() + expires_delta
        return self._jwt_service.encode(PayloadDTO(sub=user_id, exp=expire))

    def _create_access_token(self, user_id: int) -> str:
        return self._create_token(user_id, timedelta(minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES))

    def _create_refresh_token(self, user_id: int) -> str:
        return self._create_token(user_id, timedelta(days=self._REFRESH_TOKEN_EXPIRE_DAYS))

    def _create_tokens(self, user_id: int) -> TokenDTO:
        return TokenDTO(
            access_token=self._create_access_token(user_id),
            refresh_token=self._create_refresh_token(user_id)
        )

    @staticmethod
    def _create_response_user_dto(
            user: DBUser, staff_member: Optional[Staff]
    ) -> ResponseUserDTO:
        if staff_member is not None:
            role_value = staff_member.role.value
            is_staff = role_value == 'ADMIN'
            is_manager = role_value == 'MANAGER' or is_staff
        else:
            role_value = 'CLIENT'
            is_staff = False
            is_manager = False
        return ResponseUserDTO(
            id=user.id,
            email=user.email.value,
            username=user.username,
            is_staff=is_staff,
            is_manager=is_manager,
            role=role_value,
            avatar_url=user.avatar_url
        )
