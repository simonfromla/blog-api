from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object.'
    # my_safe_method = ['GET', 'PUT'] # Additional 'GET' b/c PostUpdateAPIView inherits from RetrieveUpdateAPIView

    # def has_permission(self, request, view): # Similar to instance-level _object_permission but more generic, view-level. Can be used if you weren't specifically using an object view.
    #     if request.method in self.my_safe_method:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        # my_safe_method = ['PUT']
        if request.method in SAFE_METHODS: # self.my_safe_method vs ^my_safe_method or SAFE_METHODS
            return True
        return obj.user == request.user # obj.*user* is the owner of the instance, and coming from the Post model 'user'
