from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreationSerializer(serializers.ModelSerializer):
    # 1. 보안 설정: 비밀번호는 입력만 받고, 결과값(Response)에는 절대 보여주지 않음
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'followings')
        # 2. 팔로우 설정: 가입 시점에는 내가 누구를 팔로우할 수 없으므로 읽기 전용으로 막음
        read_only_fields = ('followings',)

    # 3. 비밀번호 해싱 처리 (가장 중요 )
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class UserSerializer(serializers.ModelSerializer):
    followers = UserListSerializer(many=True, read_only=True)
    followings = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'followings', 'followers')
