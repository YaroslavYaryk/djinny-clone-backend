# Generated by Django 4.1.7 on 2023-03-07 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_alter_jobpost_experience_years_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='salary',
            field=models.IntegerField(null=True),
        ),
    ]
