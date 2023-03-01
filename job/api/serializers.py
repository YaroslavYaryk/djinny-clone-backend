from rest_framework import serializers, exceptions
from rest_framework.fields import SerializerMethodField
from job.models import JobPost, JobLocation, JobType, JobPostSkillSet, JobPostActivity, JobConversation, \
    ConversationMessage


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = "__all__"


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"


class JobPostActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostActivity
        fields = "__all__"


class JobLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLocation
        fields = "__all__"


class JobPostSkillSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostSkillSet
        fields = "__all__"


class JobConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobConversation
        fields = "__all__"


class JobConversationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobConversation
        exclude = ("creation_date",)


class ConversationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMessage
        fields = "__all__"
