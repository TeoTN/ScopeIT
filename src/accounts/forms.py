from django import forms

import autocomplete_light.shortcuts as autocomplete_light

from .models import Entity, Skill


class SkillsAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields = ('name',)
    model = Skill
autocomplete_light.register(SkillsAutocomplete)


class EntityForm(autocomplete_light.ModelForm):
    class Meta:
        autocomplete_names = {'skills': 'SkillsAutocomplete'}
        model = Entity
        fields = ['city', 'country', 'skills']