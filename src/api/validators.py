from django.contrib.auth.models import User

from rest_framework import serializers


class UserExists(object):
    def __call__(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            message = "User {} does not exist.".format(value)
            raise serializers.ValidationError(message)
