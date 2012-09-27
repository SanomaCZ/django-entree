import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from entree.client.managers import EntreeUserDBManager

from jsonfield import JSONField


ENTREE = settings.ENTREE
logger = logging.getLogger(__name__)


class EntreeDBUser(User):

    key = models.CharField("Auth key", max_length=40, db_index=True)
    userdata = JSONField(default='{}')

    objects = EntreeUserDBManager()

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:
            kwargs['userdata'] = kwargs['data']
        super(EntreeDBUser, self).__init__(*args, **kwargs)

    def get_and_delete_messages(self):
        #not available in self.__dict__, WTF?
        return []

    def __eq__(self, other):
        return self.key == other.key

    def __unicode__(self):
        return u'EntreeUser %s' % self.email

    def save(self, *args, **kwargs):
        if not self.key:
            raise ValueError("Cannot save user w/o auth key")

        self.username = self.email
        self.userdata.update({'email': self.email})
        super(EntreeDBUser, self).save(*args, **kwargs)

    def _get_data(self):
        return self.userdata

    def _set_data(self, *args):
        data = self.userdata
        data.update(args[0])
        self.userdata = data

    data = property(_get_data, _set_data)
