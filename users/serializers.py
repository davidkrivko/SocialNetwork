from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from network_config.redis import get_online_flag
from users.models import UserModel


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LastActivityUserSerializer(serializers.ModelSerializer):
    last_activity = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = (
            "id",
            "last_login",
            "last_activity",
        )

    def get_last_activity(self, obj):
        timestamp_str = get_online_flag(obj.username)[0][1]["timestamp"]
        timestamp_datetime = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f%z")

        formatted_timestamp = timezone.localtime(timestamp_datetime).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        return formatted_timestamp

