from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from .serializers import CompanySerializer, CompanyImagesSerializer, BusinessStreamSerializer
from .services import handle_company
from seeker.api.services import static_fuctions
from job.api.serializers import JobPostSerializer


class BaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        req = self.initialize_request(request, *args, **kwargs)
        response = super(BaseAPIView, self).dispatch(request, *args, **kwargs)
        if req.user.user_type.has_additional_profile:
            raise Http404

        return response


# profile
class CompanyAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        if kwargs:
            company_details = handle_company.get_company_by_for_user_by_id(kwargs["id"], request.user)
            serializer = CompanySerializer(instance=company_details)
        else:
            companies = handle_company.get_companies_for_user(request.user)
            serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        data = {**request.data, "user_account": request.user.id}
        serializer = CompanySerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        company = handle_company.get_company_by_for_user_by_id(pk, request.user)
        serializer = CompanySerializer(instance=company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        message = static_fuctions.get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        try:
            handle_company.delete_company(pk, request.user)
            return Response({"message": "successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message", str(ex)}, status=status.HTTP_403_FORBIDDEN)


class CompanyImagesAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company_images = handle_company.get_images_for_company(pk)
        serializer = CompanyImagesSerializer(company_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        data = handle_company.get_parsed_images(request.data)
        if data:
            handle_company.add_company_images(pk, data)
            return Response({"message": "successful"}, status=status.HTTP_201_CREATED)
        return Response({"message": "invalid data"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, image_id):
        try:
            handle_company.delete_company_image(image_id)
            return Response({"message": "successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message", str(ex)}, status=status.HTTP_403_FORBIDDEN)


@api_view(('DELETE',))
@permission_classes((IsAuthenticated,))
def delete_all_company_images(request, pk):
    try:
        handle_company.delete_all_images(pk)
        return Response({"message": "Successful"}, status=status.HTTP_200_OK)

    except Exception as ex:

        return Response({"message": str(ex)}, status=status.HTTP_403_FORBIDDEN)


class BusinessStreamStreamAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business_stream_queryset = handle_company.get_business_stream_queryset()
        serializer = BusinessStreamSerializer(business_stream_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyJobAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        queryset = handle_company.get_jobs_for_company(pk)
        serializer = JobPostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
