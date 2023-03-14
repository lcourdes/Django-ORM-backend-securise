from rest_framework.serializers import ModelSerializer, Serializer
from django.db import transaction
from application.models import Client
from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'company_name', 'email', 'last_name', 'is_client']


class ClientDetailSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'company_name', 'email', 'is_client', 'first_name',
                   'last_name', 'phone', 'mobile', 'date_created', 'date_updated']

    @transaction.atomic
    def create(self, data, *args, **kwargs):
        sales_contact = self.context.get('request').user        
        client = Client.objects.create(**data, sales_contact=sales_contact)
        client.save()
        return client
    
    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get('company_name'):
            instance.company_name = validated_data.get('company_name')
        if validated_data.get('is_client'):
            instance.is_client = validated_data.get('is_client')
        if validated_data.get('sales_contact'):
            instance.sales_contact = validated_data.get('sales_contact')
        if validated_data.get('email'):
            instance.email = validated_data.get('email')
        if validated_data.get('first_name'):
            instance.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            instance.last_name = validated_data.get('last_name')
        if validated_data.get('phone'):
            instance.phone = validated_data.get('phone')
        if validated_data.get('mobile'):
            instance.mobile = validated_data.get('mobile')
        instance.save()
        return instance
