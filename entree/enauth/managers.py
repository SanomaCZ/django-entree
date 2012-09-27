import logging

from django.db import models

from entree.common.managers import CachedManagerMixin


logger = logging.getLogger(__name__)


class IdentityManager(CachedManagerMixin, models.Manager):
    def create(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        pwd = kwargs.pop('password', None)
        obj = self.model(**kwargs)
        obj.set_password(pwd)
        obj.save(using=self.db)
        return obj


class LoginTokenManager(CachedManagerMixin, models.Manager):
    def get_cached(self, key, cache_prefix=""):
        token = super(LoginTokenManager, self).get_cached(key, cache_prefix)
        if token is None:
            from entree.enauth.models import LoginToken

            token = LoginToken.objects.select_related('user').get(value=key)
            self.set_cached(key=key, value=token, cache_prefix=cache_prefix)

        return token
