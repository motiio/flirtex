from calendar import timegm
from datetime import datetime

from jose import JWTError, jwt
from jose.exceptions import JWKError

from src.config.settings import settings
from src.modules.auth.domain.exceptions import InvalidJWTToken


def generate_token(*, sub: str, expiration_seconds: int, secret: str = settings.JWT_SECRET) -> str:
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
    secret: str = settings.JWT_SECRET,
) -> tuple[str, dict]:
    try:
        data = jwt.decode(token, secret, algorithms=["HS256"])
    except (JWKError, JWTError):
        raise InvalidJWTToken from None
    else:
        return token, data
