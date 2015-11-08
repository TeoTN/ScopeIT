# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=30)),
                ('certificates', models.ManyToManyField(to='accounts.Certificate')),
                ('education_tiers', models.ManyToManyField(to='accounts.EducationTier')),
                ('languages', models.ManyToManyField(to='accounts.Language')),
            ],
        ),
        migrations.RemoveField(
            model_name='professionalprofile',
            name='certificates',
        ),
        migrations.RemoveField(
            model_name='professionalprofile',
            name='education_tiers',
        ),
        migrations.RemoveField(
            model_name='professionalprofile',
            name='languages',
        ),
        migrations.RemoveField(
            model_name='professionalprofile',
            name='skills',
        ),
        migrations.RemoveField(
            model_name='professionalprofile',
            name='user_profile',
        ),
        migrations.AlterField(
            model_name='skill',
            name='type',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='profile',
            field=models.ForeignKey(to='accounts.Entity'),
        ),
        migrations.DeleteModel(
            name='ProfessionalProfile',
        ),
        migrations.AddField(
            model_name='entity',
            name='skills',
            field=models.ManyToManyField(to='accounts.Skill', through='accounts.UserSkill'),
        ),
        migrations.AddField(
            model_name='entity',
            name='user_profile',
            field=models.ForeignKey(related_name='profile_set', to='accounts.UserProfile'),
        ),
    ]
