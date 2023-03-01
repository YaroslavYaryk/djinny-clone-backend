from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from seeker.api.services import static_fuctions
from .services import handle_job_type_and_activity, handle_job_post, handle_job_location, handle_job_skillset, \
    handle_conversation

from .serializers import JobTypeSerializer, JobPostSerializer, JobPostActivitySerializer, JobLocationSerializer, \
    JobPostSkillSetSerializer, JobConversationSerializer, ConversationMessageSerializer, JobConversationPostSerializer
from .services.constants import USER_TYPES


class BaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        req = self.initialize_request(request, *args, **kwargs)
        response = super(BaseAPIView, self).dispatch(request, *args, **kwargs)
        if req.user.user_type.has_additional_profile:
            raise Http404

        return response


class JobTypeAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs:
            job_type = handle_job_type_and_activity.get_job_type_by_id(kwargs["id"])
            serializer = JobTypeSerializer(instance=job_type)
        else:
            queryset = handle_job_type_and_activity.get_all_job_types()
            serializer = JobTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobPostAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs:
            job_post = handle_job_post.get_job_post_by_id_for_user(kwargs["id"], request.user)
            print(job_post)
            serializer = JobPostSerializer(instance=job_post)
        else:
            queryset = handle_job_post.get_job_posts_for_user(request.user)
            serializer = JobPostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):

        data = {**request.data, "posted_by": request.user.id}
        serializer = JobPostSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    #
    def patch(self, request, pk):
        job_post = handle_job_post.get_job_post_by_id_for_user(pk, request.user)
        serializer = JobPostSerializer(instance=job_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    #
    def delete(self, request, pk):
        try:
            handle_job_post.delete_job_post(pk, request.user)
            return Response({"message": "successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message", str(ex)}, status=status.HTTP_403_FORBIDDEN)


class JobActivityAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        job_activity = handle_job_type_and_activity.get_activity_for_job(pk, request.user)
        serializer = JobPostActivitySerializer(instance=job_activity)

        return Response(serializer.data, status=status.HTTP_200_OK)


class JobLocationAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs.get("location_id"):
            job_location = handle_job_location.get_location_for_job(kwargs["id"], kwargs["location_id"], request.user)
            serializer = JobLocationSerializer(instance=job_location)
        else:
            queryset = handle_job_location.get_all_job_locations(kwargs["id"], request.user)
            serializer = JobLocationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):

        data = {**request.data, "job_post": pk}
        serializer = JobLocationSerializer(data=data, partial=True)
        if serializer.is_valid():
            location = serializer.save()
            location.job_post__id = pk
            location.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk, location_id):
        job_post_location = handle_job_location.get_location_for_job(pk, location_id, request.user)
        serializer = JobLocationSerializer(instance=job_post_location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, location_id):
        try:
            handle_job_location.delete_job_location(pk, location_id, request.user)
            return Response({"message": "successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message", str(ex)}, status=status.HTTP_403_FORBIDDEN)


class JobSkillSetAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        queryset = handle_job_skillset.get_job_skillset(pk)
        serializer = JobPostSkillSetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        data = handle_job_skillset.get_class_list_from_js(request.data)
        if data:
            handle_job_skillset.add_skillsets_to_job(data, pk)
            return Response({"message": "successful"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid data"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, ):
        data = handle_job_skillset.get_class_list_from_js(request.data)
        if data:
            handle_job_skillset.delete_job_skillset(pk)
            handle_job_skillset.add_skillsets_to_job(data, pk)
            return Response({"message": "successful"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid data"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        try:
            handle_job_skillset.delete_job_skillset(pk)
            return Response({"message": "successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message", str(ex)}, status=status.HTTP_403_FORBIDDEN)


class JobConversationAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs:
            conversation = handle_conversation.get_conversation_by_id(kwargs["id"], request.user)
            serializer = JobConversationSerializer(instance=conversation)
        else:
            queryset = handle_conversation.get_conversations_for_user(request.user)
            serializer = JobConversationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, job_id, user_type: USER_TYPES, user_id):
        data = handle_conversation.get_data_for_conversation(job_id, user_type, user_id, request.user)

        serializer = JobConversationPostSerializer(data=data)
        if serializer.is_valid():
            instance, _ = handle_conversation.get_or_create_conversation(serializer)
            return Response({**serializer.data, "id": instance.id}, status=status.HTTP_201_CREATED)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, conversation_id):
        try:
            handle_conversation.delete_conversation(conversation_id, request.user)
            return Response({"message": "successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message", str(ex)}, status=status.HTTP_403_FORBIDDEN)
