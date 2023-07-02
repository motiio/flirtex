import traceback

try:
    from src.v1.config.models import Base  # noqa

    # from src.auth.models import User
#     from src.profile.models import Profile, ProfileInterests, ProfilePhoto, Interest
#     from src.common.models import Region, City
except Exception:
    traceback.print_exc()
