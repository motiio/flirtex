from uuid import UUID

from src.v1.auth.repositories.user import UserRepository
from src.v1.auth.schemas.user import UserInCreateSchema, UserOutSchema
from src.v1.usecases import BaseUseCase


class GetOrCreateUser(BaseUseCase[UserRepository, UserInCreateSchema, UserOutSchema]):
    async def execute(self, *, user_data: UserInCreateSchema):
        async with self.repository as repo:
            user = await repo.get_by_tg_id(tg_id=user_data.tg_id)
            if not user:
                user = await repo.create(in_schema=user_data)
        return UserOutSchema.model_validate(user)


class ReadUser(BaseUseCase[UserRepository, UserInCreateSchema, UserOutSchema]):
    async def execute(self, *, user_id: UUID):
        async with self.repository as repo:
            user = await repo.get(entry_id=user_id)
            return UserOutSchema.model_validate(user)
