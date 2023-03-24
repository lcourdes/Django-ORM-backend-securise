from django.db import transaction
from django.contrib.auth import login, logout
from application.serializers import LoginSerializer, ClientDetailSerializer, \
    ClientSerializer, ContractSerializer, ContractDetailSerializer, \
    ContractCreateSerializer, \
    EventSerializer, EventDetailSerializer, EventCreateSerializer
from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import views
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from application.models import Client, Contract, Event
from application.permissions import IsSaler, IsSupport


class LoginView(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        content = {'message': 'Please Login'}
        return Response(content)
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    def get(self, request):
        logout(request)
        return Response('Logged out successfully.')


class ClientViewset(ModelViewSet):
    serializer_class = ClientSerializer
    detail_serializer_class = ClientDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'email']
    permission_classes = [DjangoModelPermissions | IsSaler | IsSupport]
    
    def get_queryset(self):
        queryset = Client.objects.all()
        if self.request.user.groups.filter(name='salers').exists():
            queryset = Client.objects.filter(sales_contact=self.request.user)
        if self.request.user.groups.filter(name='supporters').exists():
            events = Event.objects.filter(support_contact=self.request.user)
            for event in events:
                client_id = [event.client_id]
            queryset = queryset.filter(id__in=client_id)
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


class ContractViewset(ModelViewSet):
    serializer_class = ContractSerializer
    detail_serializer_class = ContractDetailSerializer
    create_serializer_class = ContractCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['amount', 'payment_due', 'client__last_name', 'client__email']
    permission_classes = [DjangoModelPermissions | IsSaler]
    
    def get_queryset(self):
        queryset = Contract.objects.filter(client__sales_contact=self.request.user)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return self.create_serializer_class
        if self.action in ['retrieve']:
            return self.detail_serializer_class
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = ContractCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = ContractCreateSerializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventViewset(ModelViewSet):
    serializer_class = EventSerializer
    detail_serializer_class = EventDetailSerializer
    create_serializer_class = EventCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event_date', 'client__last_name', 'client__email']
    permission_classes = [DjangoModelPermissions|IsSaler|IsSupport]
    
    def get_queryset(self):
        queryset = Event.objects.all()
        if self.request.user.groups.filter(name='salers').exists():
            queryset = queryset.filter(client__sales_contact=self.request.user)
        if self.request.user.groups.filter(name='supporters').exists():
            queryset = queryset.filter(support_contact=self.request.user)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return self.detail_serializer_class
        if self.action in ['create', 'update']:
            return self.create_serializer_class
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request):
        serializer = EventCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = EventCreateSerializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
