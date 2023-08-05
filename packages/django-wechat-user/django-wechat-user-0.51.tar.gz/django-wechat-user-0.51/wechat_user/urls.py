from django.urls import path
from .views import validate_wx_token, obtain_token, request_vercode, bind_phone


urlpatterns = [
    path("validate", validate_wx_token),
    path("obtainToken", obtain_token),
    path("me/phone", bind_phone),
    path("vercode", request_vercode),
    path("wxlogin", wxlogin)
]
