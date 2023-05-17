from datetime import datetime, timedelta
from typing import Annotated

import orjson
from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from jose.exceptions import JWKError
from sqlalchemy import and_, insert, select, update
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from src.config.core import Settings
from src.profile.models import Profile

from .models import DeviceSession, User
from .schemas import RefreshTokenSchema, UserRead, UserSchema

InvalidInitData = HTTPException(
    status_code=HTTP_400_BAD_REQUEST, detail=[{"msg": "Invalid init data"}]
)


def validate_init_data(*, init_data: str, settings: Settings) -> UserRead | None:
    try:
        data = safe_parse_webapp_init_data(
            token=settings.BOT_TOKEN,
            init_data=init_data,
            _loads=orjson.loads,
        )
        if data.get("user", {}).get("is_bot"):
            raise ValueError
    except ValueError:
        return None
    else:
        return UserSchema(**data.get("user"))


async def create_user(*, db_session, user_data: UserSchema) -> UserRead:
    user = User(**user_data.dict())
    db_session.add(user)
    await db_session.commit()
    return user


async def get_or_create_user_by_init_data(
    *, db_session, init_data: str
) -> tuple[User, Profile | None]:
    """Returns a user based on the given initData."""
    user_data = validate_init_data(init_data=init_data)
    if not user_data:
        raise InvalidInitData

    q = (
        select(User, Profile)
        .join(
            Profile, and_(User.id == Profile.owner, Profile.is_active is True), isouter=True
        )  # noqa
        .where(User.tg_id == user_data.tg_id)
    )
    user, profile = (await db_session.execute(q)).first() or (None, None)

    if user is None:
        user = await create_user(db_session=db_session, user_data=user_data)

    return user, profile


def _check_token_signature(*, token: str):
    try:
        data = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except (JWKError, JWTError) as e:
        # Raise the HTTPException without using 'from None' to propagate original error message
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=[{"msg": str(e)}])
    else:
        return token, data


def get_current_user(request: Request):
    auth_header: str = request.headers.get("Authorization")

    # Use guard clause instead of nested if statement
    if not auth_header:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=[{"msg": "Authorization header not found"}]
        )

    token = auth_header.split()[1]
    valid_token, data = _check_token_signature(token=token)
    return data["sub"]


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_refresh_token(*, db_session, refresh_token: str) -> DeviceSession | None:
    q = select(DeviceSession).where(
        DeviceSession.refresh_token == refresh_token, DeviceSession.is_active == True  # noqa
    )
    return (await db_session.execute(q)).scalars().one_or_none()


async def create_refresh_token(*, db_session, user_id, user_agent) -> RefreshTokenSchema:
    now = datetime.utcnow()
    exp = now + timedelta(seconds=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
    data = {
        "exp": exp,
        "sub": str(user_id),
    }
    new_refresh_token_value: str = jwt.encode(data, settings.JWT_SECRET, algorithm=["HS256"])
    q = (
        insert(DeviceSession)
        .values(
            user=user_id,
            refresh_token=new_refresh_token_value,
            expires_at=exp,
            user_agent=user_agent,
        )
        .returning(DeviceSession)
    )
    new_device_session = (await db_session.execute(q)).scalars().one()
    await db_session.commit()
    return RefreshTokenSchema.from_orm(new_device_session)


async def expire_refresh_token(*, db_session, refresh_token_value) -> None:
    q = (
        update(DeviceSession)
        .where(DeviceSession.refresh_token == refresh_token_value)
        .values(is_active=False)
    )
    await db_session.execute(q)


async def expire_all_refresh_tokens_by_user_id(*, db_session, user_id) -> None:
    q = (
        update(DeviceSession)
        .where(DeviceSession.user == user_id)
        .values(DeviceSession.is_active is False)
    )
    await db_session.execute(q)


async def expire_all_refresh_tokens_by_user_agent(*, db_session, user_id, user_agent) -> None:
    q = (
        update(DeviceSession)
        .where(DeviceSession.user == user_id, DeviceSession.user_agent == user_agent)
        .values(DeviceSession.is_active == False)  # noqa
    )
    await db_session.execute(q)


async def validate_refresh_token(
    *,
    db_session,
    refresh_token,
) -> tuple[str, dict]:
    device_session = await get_refresh_token(db_session=db_session, refresh_token=refresh_token)
    if not device_session:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=[{"msg": "Invalid token signature"}]
        )

    valid_token, token_date = _check_token_signature(token=device_session.refresh_token)

    return valid_token, token_date
