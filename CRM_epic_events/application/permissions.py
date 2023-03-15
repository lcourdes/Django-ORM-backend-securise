from rest_framework.permissions import BasePermission

class IsSaler(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='salers').exists():
            if view.basename == 'events':
                if request.method == 'POST':
                    return True
    
    def has_object_permission(self, request, view, obj):
        if view.basename == 'contracts':
            if obj.sales_contact == request.user:
                return True
        

class IsSupport(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='supporters').exists():
            if view.basename == 'events':
                if request.method == 'PUT':
                    return True
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='supporters').exists():
            if view.basename == 'events':
                if request.method == 'PUT':
                    if obj.support_contact == request.user:
                        return True
