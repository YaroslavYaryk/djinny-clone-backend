# Generated by Django 4.1.7 on 2023-02-26 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_company_user_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='business_stream',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.businessstream'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(max_length=100, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_website_url',
            field=models.CharField(max_length=500, null=True, verbose_name='website url'),
        ),
        migrations.AlterField(
            model_name='company',
            name='establishment_date',
            field=models.DateField(null=True, verbose_name='establishment date'),
        ),
        migrations.AlterField(
            model_name='company',
            name='profile_description',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
