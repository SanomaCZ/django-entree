from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django.conf import settings
from entree.site.models import SiteProperty, EntreeSite, SiteProfile


class SitePropertiesAdmin(admin.TabularInline):
    model = SiteProperty
    prepopulated_fields = {"slug": ("name",)}

    verbose_name_plural = _("Site properties (available only for current site)")


class ResidentBlahFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        #kwargs['queryset'] = SiteProperty.objects.filter(site__id=settings.ENTREE['NOSITE_ID'])
        kwargs['instance'] = EntreeSite.objects.get(pk=settings.ENTREE['NOSITE_ID'])
        super(ResidentBlahFormSet, self).__init__(*args, **kwargs)


class ResidentSitePropertiesAdmin(admin.TabularInline):
    model = SiteProperty
    formset = ResidentBlahFormSet
    prepopulated_fields = {"slug": ("name",)}

    verbose_name_plural = _("Resident properties (applied to all sites)")
    verbose_name = _("Resident property (applies to all sites)")

    def get_formset(self, request, obj=None, **kwargs):
        obj = EntreeSite.objects.get(pk=settings.ENTREE['NOSITE_ID'])
        return super(ResidentSitePropertiesAdmin, self).get_formset(request, obj, **kwargs)


class EntreeSiteAdmin(admin.ModelAdmin):
    inlines = [SitePropertiesAdmin, ResidentSitePropertiesAdmin]


class SitePropertyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SiteProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(EntreeSite, EntreeSiteAdmin)
admin.site.register(SiteProperty, SitePropertyAdmin)
admin.site.register(SiteProfile, SiteProfileAdmin)
