from datetime import datetime, timedelta
from typing import Optional

from src.adapters.auth.jwt_service import JWTService
from src.application.interfaces.repos.client_repository import ClientRepository
from src.application.interfaces.repos.staff_repository import StaffRepository
from src.application.interfaces.repos.user_repository import UserRepository
from src.application.interfaces.uow import UoW
from src.application.user.dto import (
    CreateUserDTO,
    CreateStaffDTO,
    ResponseUserDTO,
    UserLoginDTO,
    TokenDTO,
    UpdateUserDTO,
    PayloadDTO,
)
from src.domain.entities.user import DBUser
from src.domain.entities.staff import Staff
from src.domain.entities.client import Client
from src.domain.exceptions.jwt import InvalidCredentialsError
from src.domain.exceptions.user import (
    InvalidEmailError,
    UserIsNotExistsError,
    UserAlreadyExistsError,
    IsNotAdminError,
    InvalidPasswordError,
)
from src.domain.services.user import UserService
from src.domain.value_objects.user import UserEmail, UserPassword

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class UserInteractor:
    def __init__(
            self,
            user_repository: UserRepository,
            staff_repository: StaffRepository,
            client_repository: ClientRepository,
            uow: UoW,
            user_service: UserService,
            jwt_service: JWTService,
    ):
        self.user_repository = user_repository
        self.staff_repository = staff_repository
        self.client_repository = client_repository
        self.uow = uow
        self.user_service = user_service
        self.jwt_service = jwt_service

    async def _ensure_user_does_not_exist(self, email: str):
        if await self.user_repository.get_by_email(email):
            raise UserAlreadyExistsError(f"User with email {email} already exists.")

    async def _get_user_by_email(self, email: str) -> DBUser:
        try:
            email_vo = UserEmail(email)
        except ValueError as e:
            raise InvalidEmailError(str(e))

        user = await self.user_repository.get_by_email(email_vo.value)
        if not user:
            raise UserIsNotExistsError("User does not exist.")
        return user

    def _create_token(self, user_id: int, expires_delta: timedelta) -> str:
        expire = datetime.utcnow() + expires_delta
        return self.jwt_service.encode(PayloadDTO(sub=user_id, exp=expire))

    def _create_access_token(self, user_id: int) -> str:
        return self._create_token(user_id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    def _create_refresh_token(self, user_id: int) -> str:
        return self._create_token(user_id, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    @staticmethod
    def _create_response_user_dto(
            user: DBUser, staff_member: Optional[Staff]
    ) -> ResponseUserDTO:
        is_staff = staff_member is not None
        role = staff_member.role.value if is_staff else 'CLIENT'
        return ResponseUserDTO(
            id=user.id,
            email=user.email.value,
            username=user.username,
            profile_image=user.profile_image,
            is_staff=is_staff,
            role=role,
        )

    async def sign_up_client(self, data: CreateUserDTO) -> ResponseUserDTO:
        await self._ensure_user_does_not_exist(data.email)
        user = self.user_service.create_user(data.email, data.password)
        db_user = await self.user_repository.create(user)
        await self.client_repository.create(Client(user=db_user))
        await self.uow.commit()
        return self._create_response_user_dto(db_user, None)

    async def sign_up_staff(self, data: CreateStaffDTO) -> ResponseUserDTO:
        await self._ensure_user_does_not_exist(data.email)
        user = self.user_service.create_user(data.email, data.password)
        db_user = await self.user_repository.create(user)
        staff = Staff(user=db_user, role=data.role)
        db_staff = await self.staff_repository.create(staff)
        await self.uow.commit()
        return self._create_response_user_dto(db_user, db_staff)

    async def sign_in(self, data: UserLoginDTO, staff_auth=False) -> TokenDTO:
        user = await self._get_user_by_email(data.email)
        if not self.user_service.verify_password(data.password, user.password):
            raise InvalidPasswordError("Invalid credentials.")

        if staff_auth:
            staff = await self.staff_repository.get_by_user_id(user_id=user.id)
            if not staff or not staff.role.value:
                raise IsNotAdminError("No such staff account.")

        access_token = self._create_access_token(user.id)
        refresh_token = self._create_refresh_token(user.id)
        staff_member = await self.staff_repository.get_by_user_id(user.id)

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            role=staff_member.role.value if staff_member else 'CLIENT',
        )

    async def refresh_token(self, refresh_token: str) -> TokenDTO:
        try:
            payload = self.jwt_service.decode(refresh_token)
        except Exception as e:
            raise InvalidCredentialsError("Invalid refresh token.") from e

        user_id = payload.sub
        if not user_id:
            raise InvalidCredentialsError("Invalid refresh token payload.")

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserIsNotExistsError("User does not exist.")

        new_access_token = self._create_access_token(user.id)
        return TokenDTO(
            access_token=new_access_token,
            refresh_token=refresh_token,
        )

    async def update_profile(self, user_id: int, data: UpdateUserDTO) -> ResponseUserDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserIsNotExistsError("User does not exist.")

        if data.password:
            user.password = UserPassword(data.password)
        if data.username:
            user.username = data.username
        if data.profile_image:
            user.profile_image = data.profile_image

        await self.user_repository.update(user)
        await self.uow.commit()
        staff_member = await self.staff_repository.get_by_user_id(user_id)
        return self._create_response_user_dto(user, staff_member)

    async def get_profile(self, user_id: int) -> ResponseUserDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserIsNotExistsError("User does not exist.")

        staff_member = await self.staff_repository.get_by_user_id(user_id)
        return self._create_response_user_dto(user, staff_member)
