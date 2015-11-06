from django.db import models
from django.contrib.auth.models import User

# from django.db.models.signals import post_save
# from django.dispatch import receiver


class Skill(models.Model):
    LANGUAGE = 1024
    FRAMEWORK = 512
    LIBRARY = 256
    OS = 128
    TOOL = 64
    TECHNOLOGY = 32

    TYPES = (
        (LANGUAGE, 'Programming language'),
        (FRAMEWORK, 'Framework'),
        (LIBRARY, 'Library'),
        (OS, 'Operating system'),
        (TOOL, 'Tool / application'),
        (TECHNOLOGY, 'Technology'),
    )

    name = models.CharField(max_length=50, null=False, primary_key=True)
    type = models.IntegerField(choices=TYPES, null=False)

    def __str__(self):
        return self.name


class Language(models.Model):
    LEVELS = (
        (0, 'A1'),
        (1, 'A2'),
        (2, 'B1'),
        (3, 'B2'),
        (4, 'C1'),
        (5, 'C2'),
    )
    name = models.CharField(max_length=20, null=False, primary_key=True)
    level = models.IntegerField(choices=LEVELS, null=False)


class EducationTier(models.Model):
    DEGREES = (
        (0, 'Bachelor'),
        (1, 'Master'),
        (2, 'Doctor of Philosophy'),
        (3, 'Professor'),
    )

    degree = models.IntegerField(choices=DEGREES, null=False)
    completed = models.BooleanField()
    university = models.CharField(max_length=100, null=False) #TODO This could be normalized


class Certificate(models.Model):
    name = models.CharField(max_length=100, null=False, primary_key=True)
    authority = models.CharField(max_length=100, null=True, blank=True)
    license = models.IntegerField(null=True, blank=True)
    url = models.URLField()
    date_from = models.DateField(null=False, blank=False)
    date_to = models.DateField(null=True, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matches = models.ManyToManyField('self', symmetrical=False, related_name='rel_matched_by')
    matched_by = models.ManyToManyField('self', symmetrical=False, related_name='rel_matches')
    is_employer = models.BooleanField()

    def get_job_profiles(self):
        return self.profile_set


class ProfessionalProfile(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile_set')
    skills = models.ManyToManyField(Skill, through='UserSkill')
    city = models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=30, null=False, blank=False)
    languages = models.ManyToManyField(Language)
    education_tiers = models.ManyToManyField(EducationTier)
    certificates = models.ManyToManyField(Certificate)


class UserSkill(models.Model):
    EXPERT = 5
    ADVANCED = 4
    INTERMEDIATE = 3
    BEGINNER = 2

    LEVELS = (
        (EXPERT, 'Expert'),
        (ADVANCED, 'Advanced'),
        (INTERMEDIATE, 'Intermediate'),
        (BEGINNER, 'Beginner'),
    )

    profile = models.ForeignKey(ProfessionalProfile)
    skill = models.ForeignKey(Skill)
    level = models.IntegerField(default=0, choices=LEVELS)

"""
@receiver(post_save, sender=User)
def attach_profile(instance, created, **kwargs):
    print(instance.username)
    if created:
        new_profile = Profile()
        new_profile.user = instance
        new_profile.save()
"""