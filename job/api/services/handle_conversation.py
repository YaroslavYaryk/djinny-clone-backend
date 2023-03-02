from django.http import Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404

from job.models import ConversationMessage, JobConversation


def get_conversation_by_id(pk, user):
    conversation = get_object_or_404(JobConversation, pk=pk)

    if not (conversation.employer == user or conversation.seeker == user):
        raise Http404
    return conversation


def get_conversations_for_user(user):
    return JobConversation.objects.filter(Q(seeker=user) | Q(employer=user))


def get_data_for_conversation(job_id, user_type, user_id, request_user):
    if user_type == "employer":
        if request_user.user_type.has_additional_profile:
            raise Http404
        employer = request_user.id
        seeker = user_id
    else:
        employer = user_id
        seeker = request_user.id

    return {
        "job": job_id,
        "employer": employer,
        "seeker": seeker
    }


def get_or_create_conversation(serializer):
    job_id = serializer.data.get("job")
    employer_id = serializer.data.get("employer")
    seeker_id = serializer.data.get("seeker")
    return JobConversation.objects.get_or_create(job_id=job_id, seeker_id=seeker_id, employer_id=employer_id)


def delete_conversation(conversation_id, user):
    get_conversation_by_id(conversation_id, user).delete()


def get_message_by_id(message_id):
    return get_object_or_404(ConversationMessage, pk=message_id)


def get_messages_for_conversation(conversation_id):
    return ConversationMessage.objects.filter(conversation__id=conversation_id)


def delete_message(message_id):
    get_message_by_id(message_id).delete()
