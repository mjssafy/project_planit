from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notice

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=False, default="")
    age = serializers.IntegerField(required=False, default=0)
    gender = serializers.CharField(required=False, default="")
    phone = serializers.CharField(required=False, default="")

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'name', 'age', 'gender', 'phone')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            name=validated_data.get('name'),
            age=validated_data.get('age'),
            gender=validated_data.get('gender'),
            phone=validated_data.get('phone'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']