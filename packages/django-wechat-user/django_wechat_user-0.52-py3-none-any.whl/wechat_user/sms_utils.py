import json
import logging
import uuid

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from django.conf import settings
from rest_framework.exceptions import APIException

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(settings.DYSMS_ACCESS_KEY, settings.DYSMS_ACCESS_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)
# logger
logger = logging.getLogger(__name__)


def send_sms(phone_number, content):
    request = SendSmsRequest.SendSmsRequest()
    request.set_TemplateCode(settings.DYSMS_TEMPLATE_CODE)
    request.set_SignName(settings.DYSMS_SIGN_NAME)
    request.set_OutId(uuid.uuid1())
    request.set_PhoneNumbers(phone_number)
    request.set_TemplateParam('{"code":"%s"}' % content)
    response = acs_client.do_action_with_exception(request).decode("utf-8")
    logger.debug("do_action_with_exception: {}".format(response))
    response = json.loads(response)
    if "Code" in response and response["Code"] != "OK":
        logger.error("Send sms to {} fail, response: {}".format(phone_number, response))
        raise APIException("SMS ERROR: {}".format(response))
    logger.info("Send sms to {} success, response: {}".format(phone_number, response))
