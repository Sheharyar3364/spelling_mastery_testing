from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.models import Note
from users.models import User

class UserRegistrationSerializer(ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ["email", "name", "password", "password2", "tc"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # validating password and confirm password
    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password2')
        if password1 != password2:
            raise serializers.ValidationError("Passwords do NOT match")
        
        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"