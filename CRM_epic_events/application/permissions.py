from rest_framework.permissions import BasePermission

class IsSaler(BasePermission):        
    def has_object_permission(self, request, view, obj):
        if obj.sales_contact == request.user:
                return True
