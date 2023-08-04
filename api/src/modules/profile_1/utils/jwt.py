from calendar import timegm
from datetime import datetime

from jose import JWTError, jwt
from jose.exceptions import JWKError

from src.v1.auth.exceptions import InvalidToken
from src.v1.config.settings import settings


def generate_token(*, sub: str, expiration_seconds: int, secret: str) -> str:
    now = timegm(datetime.utcnow().utctimetuple())
    exp = now + expiration_seconds
    data = {
        "exp": exp,
        "sub": sub,
    }
    return jwt.encode(data, secret, algorithm="HS256")


def check_token_signature(
    *,
    token: str,
) -> tuple[str, dict]:
    try:
        data = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except (JWKError, JWTError):
        raise InvalidToken from None
    else:
        return token, data
