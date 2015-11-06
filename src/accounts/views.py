from django.shortcuts import redirect
from django.views.generic import TemplateView


class ProfileView(TemplateView):
    template_name="account/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('index')

        return super(ProfileView, self).dispatch(request, *args, **kwargs)
