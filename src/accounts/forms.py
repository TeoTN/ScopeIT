from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,
                                 label='First name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First name', 'autofocus': 'autofocus'}))
    last_name = forms.CharField(max_length=30,
                                label='Surname',
                                widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    email = forms.EmailField(label="Email address", required=True, help_text="Required.")

    def save(self, request):
        user = super(SignupForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        is_employer = request.POST.get('is_employer', False)
        user_profile, _ = UserProfile.objects.get_or_create(user=user, is_employer=is_employer)
        user_profile.save()
        return user
