from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .permissions import IsCEO, IsAdmin
from .models import User

from .serializers import CustomTokenObtainPairSerializer, UserDetailSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GetMeView(APIView):
    def get(self, request):
        if self.request.user.is_authenticated:
            user = self.request.user
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)



class AdminListView(ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsCEO]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['role']
    search_fields = ['first_name', 'last_name', 'email']

    def get_queryset(self):
        return User.objects.filter(role='admin')

