from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(models.Model):
    """微信会员
    """

    PLATFORM_WEB = 0  # 从web登录
    PLATFORM_MINA = 1  # 从小程序登录
    PLATFORM_CHOICES = ((PLATFORM_WEB, _("Web")), (PLATFORM_MINA, _("Mina")))

    IDENTIFIER_OPENID = 0  # 通过OPENID识别用户
    IDENTIFIER_UNIONID = 1  # 通过UnionID识别用户
    IDENTIFIER_CHOICES = ((IDENTIFIER_OPENID, _("OpenID")), (IDENTIFIER_UNIONID, _("UnionID")))

    platform = models.IntegerField(verbose_name=_("Platform"), choices=PLATFORM_CHOICES)
    identifier = models.IntegerField(verbose_name=_("Identifier"), choices=IDENTIFIER_CHOICES)
    last_logined_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    @property
    def unionid_or_none(self):
        try:
            return self.unionid
        except:
            return None

    @property
    def openids_or_none(self):
        try:
            return self.openids.all()
        except:
            return None

    def update_last_login_date(self):
        self.last_logined_at = timezone.now()
        self.save(update_fields=["last_logined_at"])

    def __str__(self):
        return (
            f"Platform: {self.platform} identifier: {self.identifier}"
            f"unionid: ${self.unionid_or_none} openids: ${self.openids_or_none}"
        )


class UserUnionId(models.Model):
    """ 会员的UnionID
    """

    owner = models.OneToOneField(
        "User",
        verbose_name=_("Union ID"),
        related_name="unionid",
        related_query_name="unionid",
        on_delete=models.CASCADE,
    )
    value = models.CharField(verbose_name=_("Open ID"), max_length=32, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"unionid: {self.value}"


class UserOpenId(models.Model):
    """会员的OpenID
    """

    owner = models.ForeignKey(
        "User", verbose_name=_("Open Id"), related_name="openids", related_query_name="openid", on_delete=models.CASCADE
    )
    value = models.CharField(verbose_name=_("Open ID"), max_length=32, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"openid: {self.value}"


class UserInfo(models.Model):

    # gender
    GENDER_UNKNOWN = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2

    # choices of gender
    GENDER_CHOICES = ((GENDER_UNKNOWN, _("Unknown")), (GENDER_MALE, _("Male")), (GENDER_FEMALE, _("Female")))

    owner = models.OneToOneField(
        "User", verbose_name=_("User"), related_name="info", related_query_name="info", on_delete=models.CASCADE
    )
    nickname = models.CharField(verbose_name=_("Nick name"), max_length=64, blank=True, null=True)
    avatar_url = models.URLField(verbose_name=_("Avatar URL"), max_length=255, blank=True, null=True)
    gender = models.SmallIntegerField(verbose_name=_("Gender"), choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    city = models.CharField(verbose_name=_("City"), max_length=32, blank=True, null=True)
    province = models.CharField(verbose_name=_("Province"), max_length=32, blank=True, null=True)
    country = models.CharField(verbose_name=_("Country"), max_length=32, blank=True, null=True)
    language = models.CharField(verbose_name=_("Language"), max_length=16, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return ("Owner: {} " "nickname: {} " "gender: {} " "country: {} " "province: {} " "country: {} ").format(
            self.owner, self.nickname, self.gender, self.country, self.province, self.city
        )


class UserMobilePhone(models.Model):
    owner = models.OneToOneField(
        "User", verbose_name=_("User"), related_name="phone", related_query_name="phone", on_delete=models.CASCADE
    )
    number = models.CharField(verbose_name=("Phone number"), max_length=16)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return "Owner: {} number: {}".format(self.owner, self.number)
