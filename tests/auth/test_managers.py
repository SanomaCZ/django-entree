from django.test import TestCase
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
#from django.test import TestCase

from entree.enauth.managers import CachedManagerMixin
from entree.enauth.models import LoginToken, Identity, MAIL_TOKEN
from nose.tools import assert_raises, assert_equals


class TestCacheMixin(TestCase):

    def setUp(self):
        super(TestCacheMixin, self).setUp()
        cache.clear()
        self.mixin = CachedManagerMixin()

    def test_mixin_prefixed_returns_none(self):
        assert_equals(None, self.mixin.get_cached('foo', cache_prefix='foo'))

    def test_mixin_prefixed_returns_value(self):
        self.mixin.set_cached('foo', 'bar', cache_prefix='foo')
        assert_equals('bar', self.mixin.get_cached('foo', cache_prefix='foo'))

    def test_mixin_prefixed_set_doesnt_raise(self):
        assert_equals(None, self.mixin.set_cached('foo', 'bar', cache_prefix='foo'))

    def test_flush_prefixed_flush_doesnt_raise(self):
        assert_equals(None, self.mixin.flush_cached('prefix', cache_prefix='foo'))


class TestAuthManagers(TestCase):

    def setUp(self):
        super(TestAuthManagers, self).setUp()

    def reset_tokens(self):
        LoginToken.objects.all().delete()
        Identity.objects.all().delete()

    def test_token_manager_raises_if_not_exists(self):
        self.reset_tokens()

        assert_raises(ObjectDoesNotExist, lambda: LoginToken.objects.get_cached(key='foobar'))

    def test_token_manager_cache_fallback_to_db(self):
        self.reset_tokens()

        token_user = Identity.objects.create()
        save_token = LoginToken.objects.create(value='FOO', user=token_user)

        get_token = LoginToken.objects.get_cached('FOO')
        assert_equals(save_token, get_token)

    def test_token_manager_different_token_type_get_success(self):
        self.reset_tokens()

        token_user = Identity.objects.create()
        save_token = LoginToken.objects.create(value='TEST2', user=token_user, token_type=MAIL_TOKEN)

        assert_equals(save_token, LoginToken.objects.get_cached(key='TEST2'))

    def test_two_same_tokens_collide(self):
        self.reset_tokens()

        token_user = Identity.objects.create()

        LoginToken.objects.create(value='COLLIDE_ME', user=token_user)

        assert_raises(IntegrityError, lambda: LoginToken.objects.create(value='COLLIDE_ME', user=token_user))
