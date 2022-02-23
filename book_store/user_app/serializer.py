from rest_framework import serializers
from .models import UserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone']
