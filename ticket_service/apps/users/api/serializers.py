from rest_framework import serializers
from users.models import User
from users import constants


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    default_error_messages = {"email_exists": constants.EMAIL_EXISTS}

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(self.error_messages["email_exists"])
        return value

    class Meta:
        model = User
        fields = (
            User.USERNAME_FIELD,
            "first_name",
            "last_name",
            "password",
            "role",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to update user  information.
    """

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        read_only_fields = ["email"]

    def update(self, instance, validated_data):
        user = super(UserUpdateSerializer, self).update(instance, validated_data)
        return user
