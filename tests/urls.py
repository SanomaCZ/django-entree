from django.conf.urls import patterns, include

urlpatterns = patterns("",
    ("^profile/", include("entree.site.urls")),
    ("^", include("entree.enauth.urls")),
)
