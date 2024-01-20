from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.deck.application.dtos.like import LikeMessageDTO
from src.modules.deck.application.dtos.match import MatchMessageDTO
from src.modules.deck.application.repositories import (
    ILikeRepository,
    IMatchRepository,
    ISkipRepository,
)
from src.modules.deck.domain.entities import Like, Match
from src.modules.notifier.application.domain.entities import LikeMessage, MatchMessage
from src.modules.notifier.application.domain.entities.de.message import MatchMessage
from src.modules.profile.application.repositories.profile import IProfileRepository
from src.modules.profile.domain.exceptions import ProfileNotFound, TargetProfileNotFound


class LikeUsecase(IUseCase):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
        like_repository: ILikeRepository,
        skip_repository: ISkipRepository,
        match_repository: IMatchRepository,
        action_notification_service: IUseCase,
    ):
        self._like_repo: ILikeRepository = like_repository
        self._skip_repo: ISkipRepository = skip_repository
        self._match_repo: IMatchRepository = match_repository
        self._profile_repo: IProfileRepository = profile_repository
        self._action_notification_service: IUseCase = action_notification_service

    async def _make_match(self, *, like_1: Like, like_2: Like) -> Match:
        match_entitie = Match.create(
            profile_1=like_1.source_profile, profile_2=like_2.source_profile
        )

        match = await self._match_repo.create(in_entity=match_entitie)
        return match

    async def execute(  # type: ignore
        self,
        *,
        user_id: UUID,
        target_profile_id: UUID,
    ) -> None:
        async with self._like_repo, self._profile_repo, self._match_repo:
            source_profile = await self._profile_repo.get_by_owner(owner_id=user_id)
            target_profile = await self._profile_repo.get(entity_id=target_profile_id)

            if not source_profile:
                raise ProfileNotFound
            if not target_profile:
                raise TargetProfileNotFound

            my_like, his_like = await self._like_repo.get_likes_by_profiles(
                target_profile=target_profile.id, source_profile=source_profile.id
            )

            _ = await self._skip_repo.delete_by_target(
                source_profile=source_profile.id,
                target_profile=target_profile.id,
            )

            # если лайк этому профилю уже был поставлен = выход
            if my_like:
                return None

            # создаем сущность Like и добавляем в DB
            like_entitie = Like.create(
                source_profile=source_profile.id, target_profile=target_profile.id
            )
            my_like = await self._like_repo.create(in_entity=like_entitie)

            # Если лайк тебе не был поставлен, то шлем уведомление и выходим
            if not his_like:
                await self._action_notification_service.execute(
                    message=LikeMessage(
                        message_type="like",
                        recipient=str(target_profile.owner_id),
                        detail=LikeMessageDTO(**source_profile.model_dump()),
                    ),
                    stream_name=str(target_profile.owner_id),
                )
                return None

                # если также был найден лайк, который поставлен тебе, то это Match
            match = await self._make_match(like_1=my_like, like_2=his_like)

            await self._action_notification_service.execute(
                message=MatchMessage(
                    message_type="match",
                    recipient=str(target_profile.owner_id),
                    detail=MatchMessageDTO(match_id=match.id, **source_profile.model_dump()),
                ),
                stream_name=str(target_profile.owner_id),
            )

            await self._action_notification_service.execute(
                message=MatchMessage(
                    message_type="match",
                    recipient=str(source_profile.owner_id),
                    detail=MatchMessageDTO(match_id=match.id, **target_profile.model_dump()),
                ).model_dump_json(),
                stream_name=str(source_profile.owner_id),
            )

