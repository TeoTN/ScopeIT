from django import forms
from .models import UserProfile


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30,
                                 label='First name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First name', 'autofocus':'autofocus'}))
    last_name = forms.CharField(max_length=30,
                                label='Surname',
                                widget=forms.TextInput(attrs={'placeholder': 'Surname'}))

    def signup(self, request, user):
        is_employer = request.POST.get('is_employer', False)
        user_profile, _ = UserProfile.objects.get_or_create(user=user, is_employer=is_employer)
        user_profile.save()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
