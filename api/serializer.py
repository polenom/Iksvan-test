from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.models import Transaction, Category
from main.settings import BASE_CATEGORIES

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title"]


class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title")

    class Meta:
        model = Transaction
        fields = ["amount", "timestamp", "category", "organization", "user", "id"]
        extra_kwargs = {
            "user": {"write_only": True},
            "id": {"read_only": True}
        }

    def create(self, validated_data):
        category, _ = validated_data["user"].categories.get_or_create(title=validated_data["category"]["title"])
        return Transaction.objects.create(
            user=validated_data["user"],
            amount=validated_data["amount"],
            organization=validated_data["organization"],
            category=category
        )

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount")if validated_data.get("amount") else instance.amount
        instance.organization = validated_data.get("organization") if validated_data.get("organization") else instance.organization
        if validated_data.get("category"):
            instance.category, _ = instance.user.categories.get_or_create(title= validated_data.get("category")["title"])
        instance.save()
        return instance




class UserSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True, read_only=True)
    balance = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["username", "password", "email", "balance", "categories"]
        extra_kwargs = {
            "password" : {"write_only": True},

        }


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            password=make_password(validated_data["password"]),
            email=validated_data["email"]
        )
        bulk = [Category(user=user, title=elem) for elem in BASE_CATEGORIES]
        Category.objects.bulk_create(bulk)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]
        read_only_fields = ["id"]
