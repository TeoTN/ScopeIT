# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(1024, 'Programming language'), (512, 'Framework'), (256, 'Library')])),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('level', models.IntegerField(default=0, choices=[(2048, 'Advanced'), (1024, 'Intermediate'), (512, 'Beginner')])),
                ('skill', models.ForeignKey(to='app_profile.Skill')),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='some_data',
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='app_profile.UserSkill'),
        ),
    ]
