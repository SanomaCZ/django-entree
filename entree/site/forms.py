from bootstrap.forms import BootstrapForm

from django import forms
from django.db import IntegrityError, transaction
from django.utils.translation import ugettext_lazy as _

from entree.site.models import SiteProperty, SiteProfile, ProfileData, ProfileDataUnique


#TODO - highlight resident properties in form!
class ProfileForm(BootstrapForm):
    """
    Form for editing Identity's profile data.
    Handles also saving into DB, which is messy but it's ideal point for \
    handling IntegrityError, which we cannot get earlies
    """

    def __init__(self, user, site, *args, **kwargs):
        """
        - initialize fields according to actual site/user

        @param user: User to which profile belongs to
        @type user: Identity
        @param site: site to which profile belongs to
        @type site: EntreeSite
        @param args: default form's args
        @type args: list
        @param kwargs: default form's kwargs
        @type kwargs: dict
        """
        self.user = user
        self.site = site

        super(ProfileForm, self).__init__(*args, **kwargs)

        self._existing_data = None
        self._site_properties = None
        self.set_fields()


    @property
    def site_properties(self):
        if self._site_properties is None:
            self._site_properties = dict( [ (one.slug, one) for one in SiteProperty.objects.get_site_props(site=self.site) ] )
        return self._site_properties

    def set_fields(self):
        profile_data = SiteProfile.objects.get_data(user=self.user, site=self.site, override_inactive=True)

        for key, one in self.site_properties.items():
            field_args = dict(
                label=one.name,
                initial=profile_data.get(one.slug, None),
                required=one.is_required
            )

            if one.value_type == 'boolean':
                field_instance = forms.BooleanField(**field_args)
            else:
                field_instance = forms.CharField(**field_args)

            self.fields[one.slug] = field_instance

    @transaction.commit_manually
    def clean(self):
        """
        Try to save data into DB.
        If we get some error, rollback and show form w/ errors

        @return: cleaned form's data
        @rtype: dict
        """
        data = self.cleaned_data

        for key, val in self.fields.items():
            try:
                self.upsert_item(key, data.get(key))
            except IntegrityError:
                self._errors[key] = self.error_class([unicode( _("Given value already taken by some other user, use different value.")) ])
                if key in self.cleaned_data:
                    del self.cleaned_data[key]
                transaction.rollback()

        transaction.commit()
        return data

    @property
    def existing_data(self):
        """
        Load existing user's profile data for current site + resident data

        @return: user's data
        @rtype: dict
        """
        if self._existing_data is None:

            site_props_ids = [one.pk for one in self.site_properties.values()]

            tmp_data = list(ProfileData.objects.filter(site_property_id__in=site_props_ids, user=self.user).select_related('site_property')) +\
                       list(ProfileDataUnique.objects.filter(site_property_id__in=site_props_ids, user=self.user).select_related('site_property'))

            self._existing_data = dict([(one.site_property.slug, one) for one in tmp_data])
        return self._existing_data

    def upsert_item(self, key, value):
        """
        Save or update one item from form into DB.
        It can eventually raise IntegrityError

        @param key: slug of profile property
        @type key: str
        @param value: value of profile property
        @type value: str

        @raise IntegrityError
        """
        site_prop = self.site_properties[key]
        if site_prop.is_unique:
            DataClass = ProfileDataUnique
        else:
            DataClass = ProfileData

        #site has property & property already exists - update
        if key in self.existing_data:
            self.existing_data[key].set_value(value, type_hint=site_prop.value_type)
        else:
            profile_data = DataClass(site_property=site_prop, user=self.user)
            profile_data.set_value( value )

        profile, created = SiteProfile.objects.get_or_create(defaults={'is_active':True}, site=self.site, user=self.user)
        if not profile.is_active:
            profile.is_active = True
            profile.save()
        elif not created:
            #TODO - fire signal to call flush_cached()
            SiteProfile.objects.flush_cached(profile.cache_key)
