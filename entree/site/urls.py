from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from entree.site.views import ProfileView, ProfileFetchView, ProfileEdit


urlpatterns = patterns('entree.site.views',
    url(r'^edit/(?P<site_id>\d+)/(?P<next_url>[\w\d=]+)/$', ProfileEdit.as_view(), name='profile_edit'),
    url(r'^edit/(?P<site_id>\d+)/$', ProfileEdit.as_view(), name='profile_edit'),

    #used only to generate appropriate link in class ShowApiView
    url(r'^edit/$', ProfileEdit.as_view(), name='profile_edit'),

    url(r'^fetch/$', csrf_exempt(ProfileFetchView.as_view()), name='profile_fetch'),
    url(r'^$', ProfileView.as_view(), name='profile')
)
