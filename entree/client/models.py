from django.conf import settings

if 'entree.client.db' in settings.INSTALLED_APPS:
    from entree.client.db.models import EntreeDBUser as EntreeUser
else:
    from entree.client.cached.models import EntreeCacheUser as EntreeUser
