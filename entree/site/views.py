import logging

from base64 import b64decode
from binascii import Error as DecodeError

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _

from entree.common.utils import calc_checksum, SHORT_CHECK
from entree.common.views import JSONResponseMixin
from entree.enauth.models import LoginToken
from entree.site.forms import ProfileForm
from entree.site.models import EntreeSite, SiteProfile


ENTREE = settings.ENTREE
logger = logging.getLogger(__name__)


def get_next_url(origin_site, next_url=None):
    try:
        site = EntreeSite.objects.get(pk=int(origin_site))
    except (EntreeSite.DoesNotExist, TypeError):
        return reverse('profile')

    try:
        url = b64decode(next_url)
        valid_url, checksum = url.split(':')
    except (KeyError, DecodeError, ValueError, TypeError):
        valid_url = ''
    else:
        if checksum != calc_checksum(valid_url, salt=site.secret, length=SHORT_CHECK):
            valid_url = ''

    return "%s/%s" % (site.url.rstrip('/'), valid_url.lstrip('/'))


class AuthRequiredMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.entree_user.is_authenticated():
            return super(AuthRequiredMixin, self).dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))


class ProfileFetchView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        """
        request.POST contains following keys:
        - token
        - site_id
        - checksum

        @return: identity data for given site (see site_id in request.POST)
        @rtype: json on success, HttpResponseForbidden on invalid input
        """
        data = self.request.POST
        try:
            site = EntreeSite.objects.get_cached(key=data['site_id'])
        except (EntreeSite.DoesNotExist, KeyError):
            logger.error("requested EntreeSite does not exist", extra={'site_id': data.get('site_id')})
            return HttpResponseForbidden(_("Invalid site id"))

        if not site.is_active:
            return HttpResponseForbidden(_("Origin site is not active"))

        expected_checksum = calc_checksum("%s:%s" % (data['site_id'], data.get('token')), salt=site.secret)
        if expected_checksum != data.get('checksum'):
            logger.error("Invalid token checksum")
            return HttpResponseForbidden(_("Invalid token checksum"))

        try:
            login_token = LoginToken.objects.get_cached(key=data['token'])
        except LoginToken.DoesNotExist:
            logger.error("Requested token doesn't exist", extra={'token': data['token']})
            return HttpResponseForbidden(_("Invalid token"))

        profile_data = SiteProfile.objects.get_data(user=login_token.user, site=site)
        profile_data.update(login_token.user.basic_data)
        return self.render_to_response(profile_data)


class ProfileEdit(AuthRequiredMixin, FormView):

    template_name = 'profile_edit.html'
    form_class = ProfileForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.site = EntreeSite.objects.get_cached(kwargs['site_id'])
        except (KeyError, EntreeSite.DoesNotExist):
            raise Http404(_("Requested site doesn't exist"))

        return super(ProfileEdit, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        data = super(ProfileEdit, self).get_form_kwargs()
        data.update({
            'site': self.site,
            'user': self.request.entree_user,
        })
        return data

    def get_context_data(self, **kwargs):
        profile, created = SiteProfile.objects.get_or_create(site=self.site, user=self.request.entree_user)

        data = super(ProfileEdit, self).get_context_data(**kwargs)
        data.update({
            'site': self.site,
            'is_active': profile.is_active
        })
        return data

    def form_valid(self, form):
        messages.success(self.request, _("Changes successfully saved"))

        next_url = self.kwargs.get('next_url')
        if not next_url:
            return HttpResponseRedirect(reverse('profile'))

        return HttpResponseRedirect(get_next_url(self.kwargs['site_id'], next_url))


class ProfileView(AuthRequiredMixin, TemplateView):

    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        data = super(ProfileView, self).get_context_data(**kwargs)
        data['sites'] = EntreeSite.objects.active()
        data['active_profiles'] = SiteProfile.objects.filter(user=self.request.entree_user, is_active=True).values_list('site_id', flat=True)
        return data
