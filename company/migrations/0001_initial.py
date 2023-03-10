# Generated by Django 4.1.7 on 2023-02-21 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_stream_name', models.CharField(max_length=100, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, verbose_name='name')),
                ('profile_description', models.TextField(max_length=1000)),
                ('establishment_date', models.DateField(verbose_name='establishment date')),
                ('company_website_url', models.CharField(max_length=500, verbose_name='website url')),
                ('business_stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.businessstream')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_image', models.ImageField(blank=True, upload_to='company_images/')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_images', to='company.company')),
            ],
        ),
    ]
