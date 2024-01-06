from dataclasses import dataclass
from uuid import UUID


@dataclass
class MatchProfileDAE:
    match_id: UUID
    profile_id: UUID
    profile_name: str
    profile_bio: str | None
    profile_main_photo_url: str | None

    @classmethod
    def create(
        cls,
        *,
        match_id: UUID,
        profile_id: UUID,
        profile_name: str,
        profile_bio: str | None = None,
        profile_main_photo_url: str | None = None,
        **kwargs,
    ) -> "MatchProfileDAE":
        match_profile_dae = cls(
            match_id=match_id,
            profile_id=profile_id,
            profile_name=profile_name,
            profile_bio=profile_bio,
            profile_main_photo_url=profile_main_photo_url,
        )
        return match_profile_dae
