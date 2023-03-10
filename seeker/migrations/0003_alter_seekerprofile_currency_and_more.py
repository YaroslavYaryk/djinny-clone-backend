# Generated by Django 4.1.7 on 2023-02-24 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seeker', '0002_alter_seekerprofile_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seekerprofile',
            name='currency',
            field=models.CharField(max_length=50, null=True, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='seekerprofile',
            name='current_salary',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='seekerprofile',
            name='first_name',
            field=models.CharField(max_length=255, null=True, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='seekerprofile',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Last name'),
        ),
    ]
