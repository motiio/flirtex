from uuid import UUID

from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from src.modules.auth.application.dependencies import CurrentUser
from src.modules.deck.api.schemas import UpdateFilterRequestSchema
from src.modules.deck.api.schemas.deck import DeckBatchOutResponse
from src.modules.deck.application.dependencies import (
    GetFilterService,
    LikeService,
    PersonalDeckService,
    SkipService,
    UpdateFilterService,
)
from src.modules.deck.application.dtos import DeckBatchOutDTO, FilterOutDTO, MatchOutDTO

# from src.modules.deck.application.dependencies.filter import GetOrCreateFilterService
# from src.modules.deck.application.dtos import DeckBatchOutDTO, FilterOutDTO
# from src.modules.deck.dependencies import PersonalDeckService, FilterGetOrCreateService

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
    profiles_batch: DeckBatchOutDTO = await personal_deck_service.execute(
        user_id=user_id
    )
    return profiles_batch


@deck_router.post(
    "/like/{target_profile}",
    response_model=MatchOutDTO | None,
    status_code=HTTP_200_OK,
)
async def like(
    user_id: CurrentUser,
    target_profile: UUID,
    like_service: LikeService,
):
    match = await like_service.execute(
        user_id=user_id,
        target_profile=target_profile,
    )
    return match


@deck_router.post(
    "/skip/{target_profile}",
    status_code=HTTP_204_NO_CONTENT,
)
async def skip(
    user_id: CurrentUser,
    target_profile: UUID,
    skip_service: SkipService,
):
    _ = await skip_service.execute(
        user_id=user_id,
        target_profile=target_profile,
    )
