__all__ = ["AuthAPI"]
from .jwt_auth_facade import JWTAuthFacade
AuthAPI = JWTAuthFacade.create()
