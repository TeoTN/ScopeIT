from django.shortcuts import render
from django.views.generic import TemplateView

class ProfileView(TemplateView):
    template_name="profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context