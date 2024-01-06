from uuid import UUID

from fastapi import APIRouter, Query
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)

from src.modules.auth.application.dependencies import CurrentUser
from src.modules.deck.api.schemas import (
    DeckBatchOutResponse,
    LikeReactionsOutSchema,
    MatchesOutSchema,
    UpdateFilterRequestSchema,
)
from src.modules.deck.application.dependencies import (
    GetFilterService,
    LikeReactionsService,
    LikeService,
    PersonalDeckService,
    SkipService,
    UpdateFilterService,
)
from src.modules.deck.application.dependencies.match import MatchService
from src.modules.deck.application.dtos import (
    DeckBatchOutDTO,
    FilterOutDTO,
)

deck_router = APIRouter(prefix="/deck")


@deck_router.patch(
    "/filter",
    response_model=FilterOutDTO,
    status_code=HTTP_200_OK,
)
async def put_filter(
    user_id: CurrentUser,
    new_filter_data: UpdateFilterRequestSchema,
    filter_update_service: UpdateFilterService,
):
    new_filter: FilterOutDTO = await filter_update_service.execute(
        in_entity=new_filter_data, user_id=user_id
    )
    return new_filter


@deck_router.get(
    "/filter",
    response_model=FilterOutDTO,
    status_code=HTTP_200_OK,
)
async def get__filter(
    user_id: CurrentUser,
    filter_service: GetFilterService,
):
    profile_filter: FilterOutDTO = await filter_service.execute(user_id=user_id)

    return profile_filter


@deck_router.post(
    "/",
    response_model=DeckBatchOutResponse,
    status_code=HTTP_200_OK,
)
async def get_deck_batch(
    user_id: CurrentUser,
    personal_deck_service: PersonalDeckService,
):
    profiles_batch: DeckBatchOutDTO = await personal_deck_service.execute(user_id=user_id)
    return profiles_batch


@deck_router.post(
    "/like/{target_profile_id}",
    status_code=HTTP_204_NO_CONTENT,
)
async def like(
    user_id: CurrentUser,
    target_profile_id: UUID,
    like_service: LikeService,
):
    await like_service.execute(
        user_id=user_id,
        target_profile_id=target_profile_id,
    )


@deck_router.post(
    "/skip/{target_profile_id}",
    status_code=HTTP_204_NO_CONTENT,
)
async def skip(
    user_id: CurrentUser,
    target_profile_id: UUID,
    skip_service: SkipService,
):
    _ = await skip_service.execute(
        user_id=user_id,
        target_profile_id=target_profile_id,
    )


@deck_router.get(
    "/matches",
    response_model=MatchesOutSchema,
    status_code=HTTP_200_OK,
)
async def matches(
    user_id: CurrentUser,
    matches_service: MatchService,
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
):
    matches, pagination = await matches_service.execute(user_id=user_id, limit=limit, offset=offset)
    return MatchesOutSchema(
        profiles=[profile.model_dump() for profile in matches.profiles], pagination=pagination
    )


@deck_router.get(
    "/like_reactions",
    response_model=LikeReactionsOutSchema,
    status_code=HTTP_200_OK,
)
async def like_reactions(
    user_id: CurrentUser,
    like_reactions_service: LikeReactionsService,
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
):
    like_reactions, pagination = await like_reactions_service.execute(
        user_id=user_id, limit=limit, offset=offset
    )
    return LikeReactionsOutSchema(
        profiles=[profile.model_dump() for profile in like_reactions.profiles],
        pagination=pagination,
    )
