from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from .forms import EntityForm


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class ProfileView(TemplateView):
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('index')

        return super(ProfileView, self).dispatch(request, *args, **kwargs)


class EntityFormView(FormView):
    template_name = 'account/entity_form.html'
    form_class = EntityForm