from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import TransactionViewSet, RegistrationUser, GetUserProfile, CategoryViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'transaction', TransactionViewSet, basename="transaction")
router.register(r"category", CategoryViewSet, basename="category")
print(router.urls)

urlpatterns = [
    path("", include(router.urls)),
    path("registration/", RegistrationUser.as_view(),),
    path("profile/", GetUserProfile.as_view()),
    path("login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
]
