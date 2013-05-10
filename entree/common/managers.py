from django.core.cache import cache


class CachedManagerMixin(object):
    cache_timeout = 1800

    @property
    def cache_key_prefix(self):
        return self.__class__.__name__

    def get_cached(self, key, cache_prefix=""):
        cache_key = "%s:%s" % (cache_prefix or self.cache_key_prefix, key)
        return cache.get(cache_key)

    def set_cached(self, key, value, cache_prefix=""):
        cache_key = "%s:%s" % (cache_prefix or self.cache_key_prefix, key)
        cache.set(cache_key, value, timeout=self.cache_timeout)

    def flush_cached(self, key, cache_prefix=""):
        cache_key = "%s:%s" % (cache_prefix or self.cache_key_prefix, key)
        cache.delete(cache_key)
