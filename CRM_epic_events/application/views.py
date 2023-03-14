from django.db import transaction
from django.contrib.auth import login
from django.shortcuts import redirect
from application.serializers import LoginSerializer, ClientDetailSerializer, ClientSerializer
from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import views
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from application.models import Client
from application.permissions import IsSaler

class LoginView(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return redirect('clients/')

class ClientViewset(ModelViewSet):
    serializer_class = ClientSerializer
    detail_serializer_class = ClientDetailSerializer
    search_fields = ['last_name', 'email']
    filter_backends = [SearchFilter]
    permission_classes = [DjangoModelPermissions | IsSaler]
    
    def get_queryset(self):
        queryset = Client.objects.filter(sales_contact=self.request.user)
        last_name = self.request.GET.get('last_name')
        if last_name is not None:
            queryset = queryset.filter(last_name=last_name)
        email = self.request.GET.get('email')
        if email is not None:
            queryset = queryset.filter(email=email)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update']:
            return self.detail_serializer_class
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request):
        serializer = ClientDetailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = ClientDetailSerializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    