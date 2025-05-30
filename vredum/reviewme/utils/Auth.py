def is_authenticated(request):
    return request.user.is_authenticated

def is_admin(request):
    return request.user.is_authenticated and request.user.is_staff

def is_superuser(request):
    return request.user.is_authenticated and request.user.is_superuser

def is_owner(request, obj):
    if not request.user.is_authenticated:
        return False
    if hasattr(obj, 'added_by'):
        return obj.added_by == request.user
    if hasattr(obj, 'user'):
        return obj.owner == request.user
    if hasattr(obj, 'created_by'):
        return obj.created_by == request.user
    return False