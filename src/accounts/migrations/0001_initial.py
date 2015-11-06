# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('authority', models.CharField(max_length=100, null=True, blank=True)),
                ('license', models.IntegerField(null=True, blank=True)),
                ('url', models.URLField()),
                ('date_from', models.DateField()),
                ('date_to', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EducationTier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('degree', models.IntegerField(choices=[(0, 'Bachelor'), (1, 'Master'), (2, 'Doctor of Philosophy'), (3, 'Professor')])),
                ('completed', models.BooleanField()),
                ('university', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('level', models.IntegerField(choices=[(0, 'A1'), (1, 'A2'), (2, 'B1'), (3, 'B2'), (4, 'C1'), (5, 'C2')])),
            ],
        ),
        migrations.CreateModel(
            name='ProfessionalProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=30)),
                ('certificates', models.ManyToManyField(to='accounts.Certificate')),
                ('education_tiers', models.ManyToManyField(to='accounts.EducationTier')),
                ('languages', models.ManyToManyField(to='accounts.Language')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1024, 'Programming language'), (512, 'Framework'), (256, 'Library'), (128, 'Operating system'), (64, 'Tool / application'), (32, 'Technology')])),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_employer', models.BooleanField()),
                ('matched_by', models.ManyToManyField(to='accounts.UserProfile', related_name='rel_matches')),
                ('matches', models.ManyToManyField(to='accounts.UserProfile', related_name='rel_matched_by')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('level', models.IntegerField(default=0, choices=[(5, 'Expert'), (4, 'Advanced'), (3, 'Intermediate'), (2, 'Beginner')])),
                ('profile', models.ForeignKey(to='accounts.ProfessionalProfile')),
                ('skill', models.ForeignKey(to='accounts.Skill')),
            ],
        ),
        migrations.AddField(
            model_name='professionalprofile',
            name='skills',
            field=models.ManyToManyField(to='accounts.Skill', through='accounts.UserSkill'),
        ),
        migrations.AddField(
            model_name='professionalprofile',
            name='user_profile',
            field=models.ForeignKey(to='accounts.UserProfile'),
        ),
    ]
