from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.database.models.staff import StaffOrm as StaffORM
from src.domain.entities.staff import Staff, DBStaff
from src.domain.value_objects.staff import StaffRole


class StaffRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, staff: Staff) -> DBStaff:
        staff_orm = StaffORM(
            user_id=staff.user.id,
            role=staff.role.value,
        )
        self.session.add(staff_orm)
        await self.session.flush()
        return DBStaff(
            id=staff_orm.id,
            user=staff.user,
            role=StaffRole(staff_orm.role),
        )

    async def get_by_user_id(self, user_id: int) -> DBStaff | None:
        result = await self.session.execute(
            select(StaffORM)
            .options(selectinload(StaffORM.user))
            .where(StaffORM.user_id == user_id)
        )
        staff_orm = result.scalar_one_or_none()
        if staff_orm:
            return DBStaff(
                id=staff_orm.id,
                user=staff_orm.user,
                role=StaffRole(staff_orm.role),
            )
        return None
