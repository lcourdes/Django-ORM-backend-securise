from rest_framework.serializers import ModelSerializer
from django.db import transaction
from django.core.exceptions import ValidationError
from application.models import Client, Contract, Event
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


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'client', 'status', 'amount', 'payment_due']


class ContractDetailSerializer(ModelSerializer):
    def validate(self, data):
        status = data['status']
        amount = data.get('amount')
        payment_due = data.get('payment_due')
        if status is False and amount is not None:
            raise ValidationError("Contract must be signed before fill amount.")
        if status is False and payment_due is not None:
            raise ValidationError("Contract must be signed before fill payment_due.")
        return data
    
    class Meta:
        model = Contract
        fields = ['id', 'status', 'amount', 'payment_due',
                   'date_created', 'date_updated']

    @transaction.atomic
    def create(self, data, *args, **kwargs):
        sales_contact = self.context.get('request').user
        client = self.context.get('client')
        contract = Contract.objects.create(**data, sales_contact=sales_contact,
                                           client=client)
        contract.save()
        return contract
    
    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get('sales_contact'):
            instance.sales_contact = validated_data.get('sales_contact')
        if validated_data.get('client'):
            instance.client = validated_data.get('client')
        if validated_data.get('status'):
            instance.status = validated_data.get('status')
        if validated_data.get('amount'):
            instance.amount = validated_data.get('amount')
        if validated_data.get('payment_due'):
            instance.payment_due = validated_data.get('payment_due')
        instance.save()
        return instance


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'client', 'event_status', 'support_contact', 'attendees',
                  'event_date']


class EventDetailSerializer(ModelSerializer):
    class Meta:
        model = Event
        read_only_fields = ['client']
        fields = ['id', 'event_status', 'support_contact', 'attendees',
                  'event_date', 'notes', 'date_created', 'date_updated']

    @transaction.atomic
    def create(self, data, *args, **kwargs):
        contract = Contract.objects.get(id=data.get('event_status').id)
        client = contract.client
        event = Event.objects.create(**data, client=client)
        event.save()
        return event
    
    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get('client'):
            instance.client = validated_data.get('client')
        if validated_data.get('event_status'):
            instance.event_status = validated_data.get('event_status')
        if validated_data.get('attendees'):
            instance.attendees = validated_data.get('attendees')
        if validated_data.get('event_date'):
            instance.event_date = validated_data.get('event_date')
        if validated_data.get('notes'):
            instance.notes = validated_data.get('notes')
        instance.save()
        return instance
