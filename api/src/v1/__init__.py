import traceback

try:
    from src.v1.base.models import Base
    from src.v1.auth.models import User, RefreshToken
    from src.v1.interest.models import Interest
    from src.v1.photo.models import Photo
    from src.v1.profile.models import Profile, ProfileInterests
    from src.v1.deck.models import Match, Like, Skip, Save
    from src.v1.location.models import ProfileLocation
except Exception:
    traceback.print_exc()
