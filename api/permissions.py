from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("has object permission")
        print(obj.user)
        print(request.user)
        
        if request.method == "GET":
            return True
        print(obj.user == request.user)
        return obj.user == request.user
    
    def has_permission(self, request, view):
        print("Has permission")
        return super().has_permission(request, view)
    
    
class CanPublish(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        print(request.user.user_permissions)
        return request.user.has_perm("post.can_publish")