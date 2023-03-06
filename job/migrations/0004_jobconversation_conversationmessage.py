# Generated by Django 4.1.7 on 2023-02-28 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0003_remove_jobpost_job_location_joblocation_job_post_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobConversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversation_employer', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job.jobpost')),
                ('seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversation_seeker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConversationMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.jobconversation')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_from_me', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job.conversationmessage')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_to_me', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
