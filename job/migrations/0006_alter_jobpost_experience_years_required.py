# Generated by Django 4.1.7 on 2023-03-06 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_jobpost_experience_years_required_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='experience_years_required',
            field=models.IntegerField(null=True),
        ),
    ]