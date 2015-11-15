# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151114_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='title',
            field=models.CharField(null=True, blank=True, max_length=30),
        ),
    ]
