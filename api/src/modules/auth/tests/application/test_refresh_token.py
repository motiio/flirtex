import os
from uuid import UUID, uuid4

import pytest

from src.modules.auth.application.dtos.telegram_login import (
    TelegramLoginOutDTO,
)
from src.modules.auth.infrastructure.models import RefreshTokenORM
from src.modules.auth.tests.infrastructure.factories.login import (
    TelegramLoginInDTOFactory,
    telegram_login_request_factory,
    telegram_login_service_factory,
)
from src.modules.auth.tests.infrastructure.factories.refresh_token_factory import (
    RefreshTokenORMFactory,
)
from src.modules.auth.tests.infrastructure.factories.user_factory import UserORMFactory


def generate_store(entities: list) -> dict:
    return {entity.id: entity for entity in entities}


EMPTY_STORE: dict = {}
EXISTS_STORE_1: dict = generate_store(
    entities=[
        UserORMFactory.create(),
        UserORMFactory.create(
            id=UUID("87501b3d-d696-4de1-8519-da5171ed5feb"),
            tg_id=99999999,
            tg_username="user_1",
            tg_first_name="FirstName1",
            tg_last_name="LastName1",
            tg_is_premium=False,
            tg_language_code="ru",
        ),
        UserORMFactory.create(id=uuid4()),
        UserORMFactory.create(id=uuid4()),
        RefreshTokenORMFactory.create(
            id=uuid4(),
            user=UUID("87501b3d-d696-4de1-8519-da5171ed5feb"),
            user_agent="ua1",
        ),
        RefreshTokenORMFactory.create(
            id=uuid4(),
            user=UUID("87501b3d-d696-4de1-8519-da5171ed5feb"),
            user_agent="ua1",
        ),
        RefreshTokenORMFactory.create(
            id=uuid4(),
            user=UUID("71d18c32-5565-4c6a-9881-2bf824cb67c6"),
            user_agent="ua1",
        ),
        RefreshTokenORMFactory.create(
            id=uuid4(),
            user=UUID("71d18c32-5565-4c6a-9881-2bf824cb67c6"),
            user_agent="ua1",
        ),
    ]
)

EXISTS_STORE_2: dict = generate_store(
    entities=[
        UserORMFactory.create(),
        UserORMFactory.create(
            id=UUID("87501b3d-d696-4de1-8519-da5171ed5feb"),
            tg_id=99999999,
            tg_username="user_1",
            tg_first_name="FirstName1",
            tg_last_name="LastName1",
            tg_is_premium=False,
            tg_language_code="ru",
        ),
        UserORMFactory.create(id=UUID("71d18c32-5565-4c6a-9881-2bf824cb67c6"), tg_id=11111111),
        UserORMFactory.create(id=uuid4()),
        RefreshTokenORMFactory.create(
            id=uuid4(),
            user=UUID("71d18c32-5565-4c6a-9881-2bf824cb67c6"),
            user_agent="ua1",
        ),
        RefreshTokenORMFactory.create(
            id=uuid4(),
            user=UUID("71d18c32-5565-4c6a-9881-2bf824cb67c6"),
            user_agent="ua1",
        ),
        RefreshTokenORMFactory.create(
            id=uuid4(),
            user=UUID("87501b3d-d696-4de1-8519-da5171ed5feb"),
            user_agent="ua1",
        ),
        RefreshTokenORMFactory.create(
            id=uuid4(),
            user=UUID("87501b3d-d696-4de1-8519-da5171ed5feb"),
            user_agent="ua1",
        ),
        RefreshTokenORMFactory.create(
            id=uuid4(),
            user=UUID("87501b3d-d696-4de1-8519-da5171ed5feb"),
            user_agent="ua1",
        ),
    ]
)


@pytest.fixture()
def tg_login_request():
    return telegram_login_request_factory(
        request_data={
            "initData": os.environ["initData"],
        },
    )


@pytest.fixture()
def store(request):
    return request.param


@pytest.mark.parametrize("store", [EMPTY_STORE, EXISTS_STORE_1, EXISTS_STORE_2], indirect=True)
@pytest.mark.asyncio
async def test_telegram_login(tg_login_request, store):
    login_service = telegram_login_service_factory(db_session=store)
    in_dto = TelegramLoginInDTOFactory.create()
    credentials: TelegramLoginOutDTO = await login_service.execute(in_dto=in_dto)
    assert ("access_token" in credentials.model_dump()) is True
    assert ("refresh_token" in credentials.model_dump()) is True


def user_agent_count(user: UUID, user_agent: str, store: dict) -> int:
    print(store)
    filtered_tokens = [
        value.user
        for value in store.values()
        if isinstance(value, RefreshTokenORM) is True
        and value.user_agent == user_agent
        and str(value.user) == str(user)
    ]
    print(filtered_tokens)

    count = sum(1 for _ in filtered_tokens)
    return count


@pytest.mark.parametrize("store", [EMPTY_STORE], indirect=True)
@pytest.mark.asyncio
async def test_telegram_login_empty_store(tg_login_request, store):
    login_service = telegram_login_service_factory(db_session=store)
    in_dto = TelegramLoginInDTOFactory.create(
        id="87501b3d-d696-4de1-8519-da5171ed5feb", user_agent="ua1"
    )
    _ = await login_service.execute(in_dto=in_dto)

    assert (
        user_agent_count(
            user=UUID("87501b3d-d696-4de1-8519-da5171ed5feb"),
            store=store,
            user_agent="ua1",
        )
        == 0
    )
    assert (len(store)) == 2


@pytest.mark.parametrize("store", [EXISTS_STORE_1, EXISTS_STORE_2], indirect=True)
@pytest.mark.asyncio
async def test_telegram_login_exists_store(tg_login_request, store):
    login_service = telegram_login_service_factory(db_session=store)
    in_dto = TelegramLoginInDTOFactory.create()
    _ = await login_service.execute(in_dto=in_dto)

    assert (
        user_agent_count(
            user=UUID("87501b3d-d696-4de1-8519-da5171ed5feb"),
            store=store,
            user_agent="ua1",
        )
        == 1
    )
    assert (
        user_agent_count(
            user=UUID("71d18c32-5565-4c6a-9881-2bf824cb67c6"),
            store=store,
            user_agent="ua1",
        )
        == 2
    )
