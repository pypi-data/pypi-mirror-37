import hashlib
import logging
import random

import arrow
import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from requests.exceptions import RequestException
from rest_framework import status, views
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .jwt_auth import (JsonWebTokenAuthentication, jwt_required,
                       obtain_json_web_token)
from .models import User, UserInfo, UserMobilePhone, UserOpenId, UserUnionId
from .serializers import UserInfoSerializer, UserSerializer
from .sms_utils import send_sms
from .wechat_api import (exchange_access_token, exchange_session_key,
                         fetch_user_info)

# logger
logger = logging.getLogger(__name__)

# 计算次数的过期时间，当天有效，所以最长为一天的秒数
DAY = 3600 * 24

# 每天最多请求多少次短消息
REQUEST_VEROODE_MAX_TIMES_PER_DAY = 10

# 验证码的位数
VERCODE_MAX_VALUE = (
    999_999 if not getattr(settings, "VERCODE_MAX_VALUE", None) else getattr(settings, "VERCODE_MAX_VALUE")
)
VERCODE_DIGIT = len(str(VERCODE_MAX_VALUE))

# 验证码的有效时间
VERCODE_EXPIRATION = (
    60 * 30 if not getattr(settings, "VERCODE_EXPIRATION", None) else getattr(settings, "VERCODE_EXPIRATION")
)


# Create your views here
@require_http_methods(["GET"])
def validate_wx_token(request):
    """验证微信设置URL时发送的token
    """
    signature = request.GET.get("signature")
    timestamp = request.GET.get("timestamp")
    nonce = request.GET.get("nonce")
    echostr = request.GET.get("echostr")
    token = settings.WECHAT_TOKEN

    string_list = [token, timestamp, nonce]
    string_list.sort()
    sha1 = hashlib.sha1()
    for string in string_list:
        sha1.update(string.encode("utf-8"))
    hashcode = sha1.hexdigest()
    return HttpResponse(echostr if hashcode == signature else "")


@api_view(["POST"])
def obtain_token(request):
    """获取token

    参数
    method: 目前只支持"code"
    platform: 目前支持 "mina" 和 "web"

    # web平台参数
    identifier:  目前支持 "openid" 和 "unionid"

    return:
        如果成功则返回{"userid": 1, "token": "xxxx"}
        web平台如果identifier为"unionid“的情况下拿不到unionid则会返回错误
    """
    method = request.data.get("method")
    platform = request.data.get("platform")
    if method not in OBTAIN_TOKEN_METHODS or platform not in OBTAIN_TOKEN_METHODS[method]:
        return Response(
            {"result": "failure", "reason": f"Unknown method: {method} for platform {platform}"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    else:
        return OBTAIN_TOKEN_METHODS[method][platform](request)


@api_view(["POST"])
@jwt_required
def request_vercode(request):
    """ 请求发送验证码

    错误码：
    -10000: 发送短消息错误
    -10001: 已经到达最大次数
    """

    user = request.authenticated_user
    phone_number = request.data.get("number")

    today = arrow.utcnow()

    times_key = "{}:vercode:{}-{}-{}:times".format(user.id, today.year, today.month, today.day)
    times = cache.get_or_set(times_key, 0, DAY)
    if times >= REQUEST_VEROODE_MAX_TIMES_PER_DAY:
        logger.info("Cant send sms to {}, Too many times: {}".format(phone_number, times))
        return Response({"result": "failure", "reason": "Max times reached", "error_code": "-10001"})

    def send_code(phone_number, code, code_key, times_key):
        try:
            send_sms(phone_number, code)
        except Exception as e:
            logger.exception(e)
            return Response({"result": "failure", "reason": "无法发送验证码，请稍后再试", "error_code": -10000})
        cache.incr(times_key)
        logger.info("Send code {} to {}, Current times: {}".format(code, phone_number, times + 1))
        return Response({"result": "success"})

    code_key = "{}:vercode:{}".format(user.id, phone_number)
    exists_code = cache.get(code_key)
    if exists_code:
        cache.expire(code_key, timeout=VERCODE_EXPIRATION)
        return send_code(phone_number, exists_code, code_key, times_key)
    else:
        code = str(random.randint(0, VERCODE_MAX_VALUE)).zfill(VERCODE_DIGIT)
        cache.set(code_key, code, timeout=VERCODE_EXPIRATION)
        return send_code(phone_number, code, code_key, times_key)


@api_view(["POST"])
@jwt_required
def bind_phone(request):
    """提交用户手机号

    错误码:
    -10000: 验证码错误
    -10001: 电话已经绑定给其他的用户
    """
    user = request.authenticated_user
    vercode = request.data.get("vercode")
    phone_number = request.data.get("number")
    code_key = "{}:vercode:{}".format(user.id, phone_number)
    exists_code = cache.get(code_key)
    if not exists_code or exists_code != vercode:
        logger.info("vercode {} not match exists coce {}".format(vercode, exists_code))
        return Response({"result": "failure", "reason": "Wrong vercode", "error_code": -10000})

    # 先检查是否已经绑定给其他的openid
    try:
        exists_user = User.objects.get(phone__number=phone_number)
        if exists_user != user:
            logger.info("Phone already bind to other user")
            return Response({"result": "failure", "reason": "Phone already bind to other user", "error_code": -10001})
        else:
            logger.info("Phone already bind to self")
            return Response({"result": "success", "warning": "Phone already bind to self"})
    except ObjectDoesNotExist:
        UserMobilePhone.objects.create(owner=user, number=phone_number)
        return Response({"result": "success"})


def obtain_token_by_code_for_web(request):
    """通过code换取token

    参考：
    https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140842
    """
    try:
        openid, access_token, refresh_token, expire_in = exchange_access_token(request.data.get("code"))

        # 抓取unionid和用户信息
        data = fetch_user_info(access_token, openid)
        identifier = request.data.get("identifier")
        user = None
        if identifier == "unionid":
            if "unionid" not in data or not data["unionid"]:
                return Response({"result": "failure", "reason": "No unionid"})
            unionid = data["unionid"]
            user, is_created = User.objects.get_or_create(
                unionid__value=unionid, defaults={"platform": 0, "identifier": 1}
            )

            if is_created:
                logger.info("create new user by unionid: {}".format(unionid))
                UserUnionId.objects.create(owner=user, value=unionid)
                user.openids.create(value=openid)
            else:
                user.update_last_login_date()
                
        elif identifier == "openid":
            user, is_created = User.objects.get_or_create(
                openid__value=openid, defaults={"platform": 0, "identifier": 0}
            )

            if is_created:
                logger.info("create new user by openid: {}".format(openid))
                user.openids.create(value=openid)
            else:
                user.update_last_login_date()
        else:
            raise APIException(f"Unknown identifier: ${identifier}")

        # 保存session到redis server
        cache.set_many(
            {"{}:accessToken".format(user.id): access_token, "{}:refreshToken".format(user.id): refresh_token},
            expire_in,
        )

        # 更新用户信息
        UserInfo.objects.update_or_create(
            owner=user,
            defaults={
                "nickname": data["nickname"],
                "avatar_url": data["headimgurl"],
                "gender": data["sex"],
                "city": data["city"],
                "province": data["province"],
                "country": data["country"],
                "language": data["language"],
            },
        )

        # 生成JWT
        token, expire_date = obtain_json_web_token(user)

        payload = UserSerializer(user).data
        # append token and expire
        payload.update({"token": token, "expire_date": expire_date.timestamp})

        # 返回 openid 给用户
        return Response({"result": "success", "payload": payload})
    except RequestException as e:
        logger.exception(e)
        return Response({"result": "failure", "reason": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def obtain_token_by_code_for_mina(request):
    """通过code换取token

    参考：
    https://developers.weixin.qq.com/miniprogram/dev/api/open-api/login/code2Session.html
    """
    try:
        openid, session_key, unionid = exchange_session_key(request.data.get("code"))
        if unionid is not None:
            user, is_created = User.objects.get_or_create(
                unionid__value=unionid, defaults={"platform": 1, "identifier": 1}
            )

            if is_created:
                logger.info("create new user by unionid: {}".format(unionid))
                UserUnionId.objects.create(owner=user, value=unionid)
                # TODO: 这里是否已经会存在相同的openid了？
                user.openids.create(value=openid)
            else:
                # openid 可能不一样，需要保存一下
                user.openids.get_or_create(value=openid, defaults={"value": openid})
                # 更新最后登陆时间
                user.update_last_login_date()

        else:
            # unionid 为空， 需要创建一个临时用户
            user, is_created = User.objects.get_or_create(
                openid__value=openid, defaults={"platform": 1, "identifier": 1}
            )
            if is_created:
                logger.info("create new user by openid: {}".format(openid))
                user.openids.create(value=openid)
            else:
                # 更新最后登陆时间
                user.update_last_login_date()

        # 保存session key
        cache.set("{}:accessToken".format(user.id), session_key)
        # 生成JWT
        token, expire_date = obtain_json_web_token(user)
        payload = UserSerializer(user).data
        # append token and expire
        payload.update({"token": token, "expire_date": expire_date.timestamp})

        # 返回 openid 给用户
        return Response({"result": "success", "payload": payload})
    except RequestException as e:
        logger.exception(e)
        return Response({"result": "failure", "reason": str(e)}, status=status.HTTP_400_BAD_REQUEST)


OBTAIN_TOKEN_METHODS = {"code": {"web": obtain_token_by_code_for_web, "mina": obtain_token_by_code_for_mina}}
