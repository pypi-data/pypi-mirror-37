"""JSON WEB TOKEN authentication
"""

import logging

import arrow
import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from functools import wraps

from .models import User

logger = logging.getLogger(__name__)


# HTTP Authentication prefix
HTTP_JWT_PREFIX = "JWT"
# JWT secret
JWT_SECRET = settings.SECRET_KEY
# algorithm
JWT_ALGORITHM = "HS256"
# jwt expire 
JWT_EXPIRE = 3600 * 24 * 30


def obtain_json_web_token(user):
    expire_date = arrow.utcnow().shift(seconds=JWT_EXPIRE)
    payload = {"id": user.id, "exp": expire_date.timestamp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM), expire_date


def payload_to_user(payload):
    user_id = payload.get("id")
    return User.objects.filter(id=user_id).first()


def decode_to_user(request):
    """从头部获取HTTP_AUTHORIZATION的值，尝试解码为用户
    """
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if not auth_header:
        return None
    # 分割字符串 JWT xxxxxxxxxx
    try:
        prefix, token = auth_header.split()
    except ValueError:
        return None
    # 检查Prefix必须为HTTP_JWT_PREFIX(JWT)
    if prefix != HTTP_JWT_PREFIX:
        return None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=(JWT_ALGORITHM,))
    except jwt.exceptions.InvalidTokenError as error:
        logger.exception(error)
        return None
    # 尝试转换为用户
    return payload_to_user(payload)


def find_user(request):
    user = decode_to_user(request)
    if user:
        request.authenticated_user = user
    return user


def jwt_required(func):
    """验证登录用户的装饰器
    """
    @wraps(func)
    def verify_login(request, *args, **kwargs):
        user = decode_to_user(request)
        if not user:
            return Response({"result": "failure", "reason": "Not authenticated!"})
        else:
            request.authenticated_user = user
            return func(request, *args, **kwargs)
    return verify_login


class JsonWebTokenAuthentication(authentication.BaseAuthentication):
    """Json web token认证器
    """
    def authenticate(self, request):
        user = decode_to_user(request)
        if not user:
            raise exceptions.AuthenticationFailed("Not authenticated")
        request.authenticated_user = user
        return (user, user.openid)
