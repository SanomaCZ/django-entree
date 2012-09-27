import logging

from django.core.exceptions import ObjectDoesNotExist
from entree.client.managers import EntreeUserCacheManager

logger = logging.getLogger(__name__)


class PseudoModelType(type):
    def __new__(mcs, name, bases, attrs):
        new_class = super(PseudoModelType, mcs).__new__(mcs, name, bases, attrs)
        ex = type('DoesNotExist', (ObjectDoesNotExist,), {})
        setattr(new_class, 'DoesNotExist', ex)
        return new_class


def pseudomodel_unpickle(model, attrs, factory):
    cls = factory(model, attrs)
    return cls.__new__(cls)
pseudomodel_unpickle.__safe_for_unpickle__ = True


def pseudomodel_factory(model, attrs):
    return model


class PseudoModel(object):
    __metaclass__ = PseudoModelType

    def __reduce__(self):
        data = self.__dict__
        model = self.__class__
        return pseudomodel_unpickle, (model, [], pseudomodel_factory), data


class EntreeCacheUser(PseudoModel):

    objects = EntreeUserCacheManager()

    def __init__(self, key=None, data=None, email=None):
        self._key = key
        self._data = data or {}
        self._data['email'] = self._data.get('email', email)
        super(EntreeCacheUser, self).__init__()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __unicode__(self):
        return u"%s %s" % (self.__class__.__name__, self.data.get('email', 'w/o ID'))

    def __str__(self):
        return str(self.__unicode__())

    def __eq__(self, other):
        a = self.key
        b = other.key
        return self.key == other.key

    def get_and_delete_messages(self):
        return []

    @property
    def key(self):
        return self._key

    def _get_data(self):
        return self._data

    def _set_data(self, data):
        self._data = data
    data = property(_get_data, _set_data)

    def save(self, *args, **kwargs):
        self.__class__.objects.set_cached(self.key, self)
