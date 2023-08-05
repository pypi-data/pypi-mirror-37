from rest_framework import serializers
from .models import User, UserInfo, UserMobilePhone


class UserMobilePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMobilePhone
        fields = ("number",)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        exclude = ("owner",)


class UserSerializer(serializers.ModelSerializer):
    info = UserInfoSerializer(required=False)
    phone = UserMobilePhoneSerializer(required=False)
    has_unionid = serializers.SerializerMethodField()

    def get_has_unionid(self, instance):
        return instance.unionid_or_none is not None

    class Meta:
        model = User
        depth = 1
        exclude = ("created_at", "last_logined_at", "identifier", "platform")
