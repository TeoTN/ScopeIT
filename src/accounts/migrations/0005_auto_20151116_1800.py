# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_entity_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='title',
            field=models.CharField(max_length=30, default='Your profile'),
        ),
    ]
