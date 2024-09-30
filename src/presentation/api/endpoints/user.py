from fastapi import APIRouter, Depends, status

from src.presentation.api.dependencies.auth import get_current_user
from src.presentation.interactor_factory import InteractorFactory
from src.domain.entities.user import DBUser
from src.application.user.dto import (
    CreateUserDTO,
    CreateStaffDTO,
    UpdateUserDTO,
    UserLoginDTO,
)
from src.presentation.api.schemas.user import (
    ResponseUserSchema,
    StaffSchema,
    TokenSchema,
    UpdateUserSchema,
    UserSchema,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/sign-up",
    response_model=ResponseUserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up_client(
        data: UserSchema, ioc: InteractorFactory = Depends()
):
    async with ioc.pick_user_interactor(lambda i: i.sign_up_client) as interactor:
        response = await interactor(
            CreateUserDTO(
                email=data.email,
                password=data.password,
            )
        )
        return response


@router.post(
    "/sign-up/staff",
    response_model=ResponseUserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up_staff(
        data: StaffSchema, ioc: InteractorFactory = Depends()
):
    async with ioc.pick_user_interactor(lambda i: i.sign_up_staff) as interactor:
        response = await interactor(
            CreateStaffDTO(
                email=data.email,
                password=data.password,
                role=data.role,
            )
        )
        print(response)
        return response


@router.post("/sign-in", response_model=TokenSchema)
async def sign_in(
        data: UserSchema,
        ioc: InteractorFactory = Depends(),
):
    async with ioc.pick_user_interactor(lambda i: i.sign_in) as interactor:
        token_dto = await interactor(
            UserLoginDTO(
                email=data.email,
                password=data.password,
            ),
            staff_auth=False,
        )
        return token_dto


@router.post("/sign-in/staff", response_model=TokenSchema)
async def sign_in_admin(
        data: UserSchema, ioc: InteractorFactory = Depends()
):
    async with ioc.pick_user_interactor(lambda i: i.sign_in) as interactor:
        token_dto = await interactor(
            UserLoginDTO(
                email=data.email,
                password=data.password,
            ),
            staff_auth=True,
        )
        return TokenSchema(
            access_token=token_dto.access_token,
            refresh_token=token_dto.refresh_token,
            role=token_dto.role
        )


@router.get("/me", response_model=ResponseUserSchema)
async def get_profile(
        current_user: DBUser = Depends(get_current_user), ioc: InteractorFactory = Depends()
):
    async with ioc.pick_user_interactor(lambda i: i.get_profile) as interactor:
        response = await interactor(current_user.id)
        return response


@router.put("/me", response_model=ResponseUserSchema)
async def update_profile(
        data: UpdateUserSchema,
        current_user: DBUser = Depends(get_current_user),
        ioc: InteractorFactory = Depends(),
):
    async with ioc.pick_user_interactor(lambda i: i.update_profile) as interactor:
        update_dto = UpdateUserDTO(
            password=data.password,
            username=data.username,
            avatar_id=data.avatar_id
        )
        response = await interactor(current_user.id, update_dto)
        return response


@router.post("/refresh-token", response_model=TokenSchema)
async def refresh_token(
        refresh_token: str, ioc: InteractorFactory = Depends()
):
    async with ioc.pick_user_interactor(lambda i: i.refresh_token) as interactor:
        token_dto = await interactor(refresh_token)
        return token_dto
