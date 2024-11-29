from rest_framework import serializers

from apps.user.models import User


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "username", "email", "name", "surname", "avatar_url", "created_at", "updated_at",
        )
        read_only_fields = ['id', "created_at", "updated_at"]

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            "username", "email", "password", "password_confirm"
        )

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user