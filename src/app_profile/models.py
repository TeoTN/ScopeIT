from django.db import models
from django.contrib.auth.models import User

# from django.db.models.signals import post_save
# from django.dispatch import receiver


class Skill(models.Model):
    PROGRAMMING_LANGUAGE = 1024
    FRAMEWORK = 512
    LIBRARY = 256
    LANGUAGE = 128
    GENERAL = 0

    TYPES = (
        (PROGRAMMING_LANGUAGE, 'Programming language'),
        (FRAMEWORK, 'Framework'),
        (LIBRARY, 'Library'),
    )

    name = models.CharField(max_length=50, null=False, primary_key=True)
    type = models.IntegerField(default=GENERAL, choices=TYPES)


class UserSkill(models.Model):
    ADVANCED = 2048
    INTERMEDIATE = 1024
    BEGINNER = 512

    LEVELS = (
        (ADVANCED, 'Advanced'),
        (INTERMEDIATE, 'Intermediate'),
        (BEGINNER, 'Beginner'),
    )

    skill = models.ForeignKey(Skill, null=False)
    level = models.IntegerField(default=0, choices=LEVELS)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(UserSkill)


"""
@receiver(post_save, sender=User)
def attach_profile(instance, created, **kwargs):
    print(instance.username)
    if created:
        new_profile = Profile()
        new_profile.user = instance
        new_profile.save()
"""