from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from application.models import User

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

admin.site.register(User, UserAdministrators)
