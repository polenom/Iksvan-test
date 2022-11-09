from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User


class GetTokensForUser:
    def get_tokens(self, user: User) -> dict:
        tokens = RefreshToken.for_user(user)
        return {
            "access": str(tokens.access_token),
            "refresh": str(tokens)
        }