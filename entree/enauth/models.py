import logging

from random import randint
from sys import maxint
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import check_password

from entree.common.models import CachedModel
from entree.enauth.managers import IdentityManager, LoginTokenManager
from entree.common.utils import calc_checksum

from app_data.fields import AppDataField


logger = logging.getLogger(__name__)

MAIL_COOLDOWN = 10 * 60  # 10 minutes
MAIL_TOKEN = 'MAIL'
AUTH_TOKEN = 'AUTH'
RESET_TOKEN = 'RESET'

TOKEN_TYPES = (
    (AUTH_TOKEN, _(AUTH_TOKEN)),
    (MAIL_TOKEN, _(MAIL_TOKEN)),
    (RESET_TOKEN, _(RESET_TOKEN)),
)
DEFAULT_TOKEN = AUTH_TOKEN


class LoginToken(CachedModel):
    """
    Tokens used for various authorisation operations
    """
    user = models.ForeignKey("enauth.Identity")
    value = models.CharField(_("Auth token"), max_length=40, unique=True)
    token_type = models.CharField(_("Token type"), choices=TOKEN_TYPES, max_length=5, db_index=True, default=DEFAULT_TOKEN)
    touched = models.DateTimeField(_("Datetime of creation"), default=datetime.now)

    app_data = AppDataField(_("Extra data for token"))

    objects = LoginTokenManager()

    @property
    def cache_key(self):
        """
        used by CachedModel as a key for caching

        @return: LoginToken is cached by its value, not pk
        @rtype: string
        """
        return self.value


class Identity(CachedModel):
    """
    Main class of user's account
    """
    email = models.EmailField("E-mail address", unique=True)
    password = models.CharField(_('password'), max_length=128)
    is_active = models.BooleanField(_('Identity active'), default=False)
    mail_verified = models.BooleanField(_('Mail verified'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=datetime.now)

    objects = IdentityManager()

    class Meta:
        verbose_name = _("User identity")

    def __unicode__(self):
        return u"Identity %s" % self.email

    def create_token(self, token_type=DEFAULT_TOKEN, app_data=None):
        """
        Helper for creating LoginToken for given Identity

        @type token_type:   string
        @param token_type:  type of token to create, should be listed in TOKEN_TYPES
        @type app_data:   dict
        @param app_data:  custom extra data to store in LoginToken.app_data

        @rtype:     LoginToken
        @return:    LoginToken w/ data based on input
        """
        if token_type not in dict(TOKEN_TYPES).keys():
            raise ValueError("Unable to create token, unknown type")

        value = calc_checksum(self.email, salt=randint(0, maxint))

        return LoginToken.objects.create(user=self, value=value, token_type=token_type, app_data=app_data)

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        if not self.is_active:
            LoginToken.objects.filter(token_type=AUTH_TOKEN, user=self).delete()
        super(Identity, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()
        return check_password(raw_password, self.password, setter)

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def is_authenticated(self):
        return True

    @property
    def basic_data(self):
        return {
            'email': self.email,
        }
