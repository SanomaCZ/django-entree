import logging

from django.conf import settings
from django.db import models

from entree.common.managers import CachedManagerMixin

from cache_tools.utils import get_cached_object


logger = logging.getLogger(__name__)
NOSITE_ID = settings.ENTREE['NOSITE_ID']


class SiteProfileManager(CachedManagerMixin, models.Manager):

    #TODO move into ProfileData
    def get_data(self, user, site=None, cascade=True, override_inactive=False):
        """
        cascade - obtain resident data as well
        override_inactive - obtain data even if profile is not active
        """
        from entree.site.models import EntreeSite
        site = site or get_cached_object(EntreeSite, pk=NOSITE_ID)

        profile, created = self.get_or_create(defaults={'is_active': False}, user=user, site=site)

        if not profile.is_active and not override_inactive:
            return {'is_active': False}

        #obtain resident profile's data?
        if cascade and site.pk != NOSITE_ID:
            generic_data = self.get_data(override_inactive=True, user=user)
        else:
            generic_data = {}

        site_data = self.get_cached(key=profile.cache_key)
        site_data['is_active'] = profile.is_active
        generic_data.update(site_data)

        return generic_data

    def get_cached(self, key, cache_prefix=""):
        """

        @param key: dict with models (user, site) to define cache key
        @type key: dict

        @param cache_prefix: key used as a cache prefix
                            (if empty,  self.__class__.__name__ is used)
        @type cache_prefix: str

        @return: cached data for SiteProfile
        @rtype: dict
        """
        hash_key = "%s:%s" % (key['user'].pk, key['site'].pk)
        data = super(SiteProfileManager, self).get_cached(hash_key, cache_prefix)

        if data is None:
            from entree.site.models import ProfileData, ProfileDataUnique, SiteProperty
            props = SiteProperty.objects.get_site_props(site=key['site'], cascade=False)

            data_items = list(ProfileData.objects.filter(site_property__in=props, user=key['user'])) + \
                    list(ProfileDataUnique.objects.filter(site_property__in=props, user=key['user']))

            data = {}
            for one in data_items:
                data[one.site_property.slug] = one.value

            for one in props:
                if one.slug not in data:
                    data[one.slug] = ""

            self.set_cached(hash_key, data)
        return data

    def flush_cached(self, key, cache_prefix=""):
        key = "%s:%s" % (key['user'].pk, key['site'].pk)
        return super(SiteProfileManager, self).flush_cached(key, cache_prefix)



class EntreeSiteManager(CachedManagerMixin, models.Manager):

    def active(self):
        return self.get_query_set().filter(is_active=True).exclude(pk=NOSITE_ID)

    def get_cached(self, key, cache_prefix=""):
        data = super(EntreeSiteManager, self).get_cached(key, cache_prefix=cache_prefix)
        if data is None:
            data = self.get_query_set().get(pk=key)
            self.set_cached(key, data, cache_prefix=cache_prefix)

        return data


class SitePropertyManager(CachedManagerMixin, models.Manager):

    def get_site_props(self, site=None, cascade=True):
        """
        @type site:  EntreeSite
        @param site: Site which attributes belongs to
        @type cascade:  boolean
        @param cascade: get also resident attributes (don't belong to any specific site)

        @rtype list
        @return list of SiteProperty items according to site_id given on input
        """
        from entree.site.models import EntreeSite
        site = site or get_cached_object(EntreeSite, pk=NOSITE_ID)

        if cascade and site.pk != NOSITE_ID:
            resident_props = self.get_site_props(cascade=False)
        else:
            resident_props = []

        site_props = self.get_cached(site.pk)
        return site_props + resident_props

    def get_cached(self, key, cache_prefix=""):
        data = super(SitePropertyManager, self).get_cached(key, cache_prefix)
        if data is None:
            data = list(self.get_query_set().filter(site_id=key))
            self.set_cached(key, value=data, cache_prefix=cache_prefix)
        return data
