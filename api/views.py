from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from api.mixins import GetTokensForUser
from api.models import Transaction
from api.permission import IsAuthor
from api.serializer import TransactionSerializer, UserSerializer, CategorySerializer

User = get_user_model()
# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthor,]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class RegistrationUser(generics.CreateAPIView, GetTokensForUser):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            validate_password(serializer.validated_data['password'])
        except ValidationError as e:
            return Response({"password": e.messages}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        tokens = self.get_tokens(user)
        headers = self.get_success_headers(serializer.data)
        return Response({**serializer.data, "tokens": tokens }, status=status.HTTP_201_CREATED, headers=headers)


class GetUserProfile(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthor, ]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.request.user.categories.all()
