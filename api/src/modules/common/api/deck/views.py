from fastapi import APIRouter, BackgroundTasks
from starlette.status import HTTP_204_NO_CONTENT

from src.v1.auth.dependencies.user import CurrentUser
from src.v1.config.database import DbSession
from src.v1.deck.bg_tasks import check_match
from src.v1.deck.dtos import LikeRequest, SkipRequest
from src.v1.deck.repositories.db import LikeRepository, SaveRepository, SkipRepository
from src.v1.deck.schemas import (
    LikeInCreateSchema,
    SaveInCreateSchema,
    SkipInCreateSchema,
)
from src.v1.deck.usecases import CreateLike, CreateSave, CreateSkip
from src.v1.profile.repositories.db import ProfileRepository
from src.v1.profile.schemas import ProfileOutReadSchema
from src.v1.profile.usecases import GetProfile, GetUserProfile

deck_router = APIRouter(prefix="/deck")


@deck_router.post(
    "/like",
    status_code=HTTP_204_NO_CONTENT,
)
async def like(
    like: LikeRequest,
    current_user_id: CurrentUser,
    db_session: DbSession,
    worker: BackgroundTasks,
):
    profile: ProfileOutReadSchema = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    liked_profile: ProfileOutReadSchema = await GetProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(profile_id=like.profile)

    like_data = LikeInCreateSchema(
        source_profile=profile.id,
        target_profile=liked_profile.id,
    )

    await CreateLike(repository=LikeRepository(db_session=db_session)).execute(in_schema=like_data)
    worker.add_task(
        check_match,
        db_session=db_session,
        source_profile=profile.id,
        target_profile=liked_profile.id,
    )


@deck_router.post(
    "/skip",
    status_code=HTTP_204_NO_CONTENT,
)
async def skip(
    skip: SkipRequest,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    profile: ProfileOutReadSchema = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    skiped_profile: ProfileOutReadSchema = await GetProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(profile_id=skip.profile)

    skip_data = SkipInCreateSchema(source_profile=profile.id, target_profile=skiped_profile.id)

    await CreateSkip(repository=SkipRepository(db_session=db_session)).execute(in_schema=skip_data)


@deck_router.post(
    "/save",
    status_code=HTTP_204_NO_CONTENT,
)
async def save(
    save: SkipRequest,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    profile: ProfileOutReadSchema = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    saved_profile: ProfileOutReadSchema = await GetProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(profile_id=save.profile)

    save_data = SaveInCreateSchema(source_profile=profile.id, target_profile=saved_profile.id)

    await CreateSave(repository=SaveRepository(db_session=db_session)).execute(in_schema=save_data)
