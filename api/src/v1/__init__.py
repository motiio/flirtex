import traceback

try:
    from src.v1.models import Base
    from src.v1.auth.models import User, RefreshToken
    from src.v1.profile.models import Profile, ProfilePhoto, ProfileInterests, Interest
except Exception:
    traceback.print_exc()
