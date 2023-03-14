from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .serializers import SeekerProfileSerializer, EducationDetailSerializer, ExperienceDetailSerializer, \
    SkillSetSerializer, SeekerSkillsetGetSerializer
from .services import handle_seeker_profile, handle_seeker_education, static_fuctions, handle_seeker_experience, \
    handle_skillset, handle_seeker_job
from job.api.serializers import JobPostSerializer


class BaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        req = self.initialize_request(request, *args, **kwargs)
        response = super(BaseAPIView, self).dispatch(request, *args, **kwargs)
        if not req.user.user_type.has_additional_profile:
            raise Http404

        return response


# profile
class SeekerProfileAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seeker_profile = handle_seeker_profile.get_seeker_profile_by_user_account(request.user)
        serializer = SeekerProfileSerializer(instance=seeker_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        seeker_profile = handle_seeker_profile.get_seeker_profile_by_user_account(request.user)
        serializer = SeekerProfileSerializer(instance=seeker_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": serializer.error_messages}, status=status.HTTP_403_FORBIDDEN)


# education
class EducationDetailsAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs:
            seeker_education = handle_seeker_education.get_one_education_for_user(request.user, pk=kwargs["id"])
            serializer = EducationDetailSerializer(instance=seeker_education)
        else:

            educations_queryset = handle_seeker_education.get_educations_for_user(request.user)
            serializer = EducationDetailSerializer(educations_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        seeker_profile = handle_seeker_profile.get_seeker_profile_by_user_account(request.user)

        data = {**request.data, "profile_account": seeker_profile.id}
        serializer = EducationDetailSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        education_object = handle_seeker_education.get_education_by_id(pk)
        serializer = EducationDetailSerializer(instance=education_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        try:
            handle_seeker_education.delete_education(pk)
            return Response({"message": "Successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": ex}, status=status.HTTP_403_FORBIDDEN)


# experiance
class ExperienceDetailsAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs:
            seeker_experience = handle_seeker_experience.get_one_experience_for_user(request.user, pk=kwargs["id"])
            serializer = ExperienceDetailSerializer(instance=seeker_experience)
        else:

            experience_queryset = handle_seeker_experience.get_experience_for_user(request.user)
            serializer = ExperienceDetailSerializer(experience_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        seeker_profile = handle_seeker_profile.get_seeker_profile_by_user_account(request.user)
        data = {**request.data, "profile_account": seeker_profile.id}
        serializer = ExperienceDetailSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        experience_object = handle_seeker_experience.get_experience_by_id(pk)
        serializer = ExperienceDetailSerializer(instance=experience_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        try:
            handle_seeker_experience.delete_experience(pk)
            return Response({"message": "Successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": ex}, status=status.HTTP_403_FORBIDDEN)


# skillset
class SkillSetAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs:
            skill = handle_skillset.get_skillset_by_id(kwargs["id"])
            serializer = SkillSetSerializer(instance=skill)
        else:

            skills = handle_skillset.get_all_skill_sets()
            serializer = SkillSetSerializer(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# seeker skillset
class SeekerSkillsetAPIView(BaseAPIView):

    def get(self, request):
        queryset = handle_skillset.get_seeker_skillset(request.user)
        serializer = SeekerSkillsetGetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = static_fuctions.turn_js_list_objects_to_python(request.data)
        if data:
            handle_skillset.add_skillsets_to_seeker_skillset(request.user, data)
            return Response({"result": request.data, "message": "Successful"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid data"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        data = static_fuctions.turn_js_list_objects_to_python(request.data)
        if data:
            handle_skillset.delete_seeker_skillset(request.user)
            handle_skillset.add_skillsets_to_seeker_skillset(request.user, data)
            return Response({"result": request.data, "message": "Successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid data"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        try:
            handle_skillset.delete_seeker_skillset(request.user)
            return Response({"message": "Successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": ex}, status=status.HTTP_403_FORBIDDEN)


class BaseListView(ListAPIView):

    def dispatch(self, request, *args, **kwargs):
        req = self.initialize_request(request, *args, **kwargs)
        response = super(BaseListView, self).dispatch(request, *args, **kwargs)
        if not req.user.user_type.has_additional_profile:
            raise Http404

        return response


class RecommendedJobsAPIView(BaseListView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return handle_seeker_job.get_recommended_jobs_for_seeker(self.request.user)


class SearchJobsAPIView(BaseListView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return handle_seeker_job.get_searched_jobs(self.request.data, self.request.user)
