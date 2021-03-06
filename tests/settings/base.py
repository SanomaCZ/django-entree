from os.path import dirname, join

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        }
}

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'entree.site',
    'entree.enauth',
    'entree.client',
    #'entree.client.cached',
    'entree.client.db',
    'entree.common',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
)



ENTREE = {
    "ROUTE": {
        "PROFILE": "/profile/",
        "PROFILE_FETCH": "/profile/fetch/",
        "REGISTER": "/register/",
        "JS_LIB": "/static/js/entree.js",
        "LOGOUT": "/logout/",
        "LOGIN": "/login/",
        "PROFILE_EDIT": "/profile/edit/1/"
    },
    "SITE_ID": 1,
    "VERSION": 1,
    "COOKIE": {
        "PATH": "/",
        "ANONYMOUS_VALUE": "ANONYMOUS",
        "INVALID": "INVALID",
        "NAME": "entree_token",
        "DOMAIN": "foobar"
    },
    "URL_SERVER": "http://foobar:8090",
    "SECRET_KEY": "REPLACE_ME",
    "CACHE_PROFILE": 300,

    'NOSITE_ID': 100, #EntreeSite, wthich acts as no-site (generic attributes purpose) (SERVER)
    'SESSION_KEY': 'entree_session',
    'STORAGE_TOKEN_KEY': 'entree_token', #localstorage's key which contains token (SERVER)
    'DEFAULT_SITE': 2,
}


try:
    from settings.local import *
except ImportError:
    pass

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
    }

ROOT_URLCONF = 'tests.urls'


TEMPLATE_DIRS = (
    join(dirname(__file__), '..', 'templates'),
)

DEFAULT_FROM_MAIL ='foo@bar.cz'

STATIC_URL = 'foo'

MESSAGE_STORAGE = 'django.contrib.messages.storage.base.BaseStorage'
