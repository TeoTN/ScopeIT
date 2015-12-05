# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20151116_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='matched_by',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='matches',
        ),
        migrations.AddField(
            model_name='entity',
            name='match',
            field=models.ForeignKey(null=True, to='accounts.Entity'),
        ),
    ]
