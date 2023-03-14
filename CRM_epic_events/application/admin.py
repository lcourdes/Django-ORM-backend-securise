from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from application.models import User, Client

class UserAdministrators(UserAdmin):
    list_display = ('id', 'username', 'last_name', 'first_name', 'email')  
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'first_name', 
                       'last_name', 'groups', 'is_staff')}
        ),
    )
    list_filter = ['last_name', 'groups']


class ClientAdministrators(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'is_client', 'sales_contact')
    search_fields = ['company_name', 'last_name', 'email', 'sales_contact__username']


admin.site.register(Client, ClientAdministrators)
admin.site.register(User, UserAdministrators)
