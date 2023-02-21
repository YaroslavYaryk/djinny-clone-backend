# Generated by Django 4.1.7 on 2023-02-21 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SeekerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('current_salary', models.IntegerField()),
                ('is_annually_monthly', models.BooleanField(default=True)),
                ('currency', models.CharField(max_length=50, verbose_name='Currency')),
                ('user_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Account')),
            ],
        ),
        migrations.CreateModel(
            name='SkillSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='skill set name')),
            ],
        ),
        migrations.CreateModel(
            name='SeekerSkillSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.IntegerField()),
                ('profile_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seeker_skill_set', to='seeker.seekerprofile')),
                ('skill_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seeker.skillset')),
            ],
            options={
                'unique_together': {('profile_account', 'skill_set')},
            },
        ),
        migrations.CreateModel(
            name='ExperienceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_current_job', models.BooleanField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('job_title', models.CharField(max_length=50, verbose_name='Job title')),
                ('company_name', models.CharField(max_length=50, verbose_name='Company name')),
                ('job_location_city', models.CharField(max_length=50, verbose_name='City')),
                ('job_location_state', models.CharField(max_length=50, verbose_name='state')),
                ('job_location_country', models.CharField(max_length=50, verbose_name='country')),
                ('description', models.TextField(max_length=4000)),
                ('profile_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seeker_experiences', to='seeker.seekerprofile')),
            ],
            options={
                'unique_together': {('profile_account', 'start_date', 'end_date')},
            },
        ),
        migrations.CreateModel(
            name='EducationDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_degree_name', models.CharField(max_length=50)),
                ('major', models.CharField(max_length=50)),
                ('institute_university_name', models.CharField(max_length=50)),
                ('starting_date', models.DateField()),
                ('completion_date', models.DateField()),
                ('percentage', models.FloatField()),
                ('cgpa', models.FloatField()),
                ('profile_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seeker_educations', to='seeker.seekerprofile')),
            ],
            options={
                'unique_together': {('profile_account', 'certificate_degree_name', 'major')},
            },
        ),
    ]
