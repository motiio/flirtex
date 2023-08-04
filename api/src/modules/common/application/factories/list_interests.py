from src.config.database import DbSession
from src.modules.common.application.usecases import ListInterestUsecase
from src.modules.profile.infrastructure.repositories import InterestRepository


def list_interests_service_factory(db_session: DbSession):
    interest_repository = InterestRepository(db_session=db_session)

    return ListInterestUsecase(interest_repository=interest_repository)
