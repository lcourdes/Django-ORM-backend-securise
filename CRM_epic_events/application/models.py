from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.permissions import DjangoModelPermissions


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=25)
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)

def limit_users_sales_contact():
        all_sales_contact = models.Q(groups__name='salers')
        return all_sales_contact

class Client(models.Model):
    company_name = models.CharField(max_length=250)
    is_client = models.BooleanField(default=False)
    sales_contact = models.ForeignKey(User, on_delete=models.PROTECT, 
                                      limit_choices_to=limit_users_sales_contact)
    email = models.EmailField(unique=True, max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25,blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20,blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
