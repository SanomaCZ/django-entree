import logging

from app_data.fields import AppDataField

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from entree.client.managers import EntreeUserDBManager


ENTREE = settings.ENTREE
logger = logging.getLogger(__name__)


class EntreeDBUser(AbstractBaseUser):

    key = models.CharField("Auth key", max_length=40, db_index=True, unique=True)
    app_data = AppDataField()

    objects = EntreeUserDBManager()

    USERNAME_FIELD = 'username'

    def get_and_delete_messages(self):
        #this is not available in self.__dict__, WTF?
        return []

    def __eq__(self, other):
        return self.key == other.key

    def __unicode__(self):
        return u'EntreeUser %s' % self.email
