# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20151108_2116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entity',
            options={'verbose_name_plural': 'entities'},
        ),
    ]
