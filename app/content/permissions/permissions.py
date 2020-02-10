from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission, SAFE_METHODS

from app.content.models import User


class IsMember(BasePermission):
    """ Checks if the user is a member """
    message = 'You are not a member'

    def has_permission(self, request, view):
        # Check if session-token is provided
        user_id = get_user_id(request)

        if user_id is None:
            return False

        return True


class IsDev(BasePermission):
    """ Checks if the user is in HS or Drift """
    message = 'You are not in DevKom'

    def has_permission(self, request, view):
        return check_group_permission(request, ['DevKom'])


class IsHS(BasePermission):
    """ Checks if the user is in HS or Drift """
    message = 'You are not in HS'

    def has_permission(self, request, view):
        return check_group_permission(request, ['HS', 'DevKom'])


class IsPromo(BasePermission):
    """ Checks if the user is in HS, Drift, or Promo """
    message = 'You are not in Promo'

    def has_permission(self, request, view):
        return check_group_permission(request, ['HS', 'DevKom' 'Promo'])


class IsNoK(BasePermission):
    """ Checks if the user is in HS, Drift, or NoK """
    message = 'You are not in NoK'

    def has_permission(self, request, view):
        return check_group_permission(request, ['HS', 'DevKom', 'NoK'])


class IsNoKorPromo(BasePermission):
    """ Checks if the user is in HS, Drift, or NoK """
    message = 'You are not in NoK'

    def has_permission(self, request, view):
        return check_group_permission(request, ['HS', 'DevKom', 'NoK', 'Promo'])


class UserPermission(BasePermission):
    """ Checks if user is admin or getting own self """
    message = "You are not an admin"

    def has_permission(self, request, view):
        get_user_id(request)

        if view.action == 'list':
            return is_admin_user(request)
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        get_user_id(request)

        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj == request.user or is_admin_user(request)
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or is_admin_user(request)
        elif view.action == 'destroy':
            return is_admin_user(request)
        else:
            return False


def check_group_permission(request, groups):
    # Allow GET, HEAD or OPTIONS requests
    if request.method in SAFE_METHODS:
        return True

    # Check if session-token is provided
    user_id = get_user_id(request)

    if user_id is None:
        return False

    # Check if user with given id is connected to Groups
    return User.objects.filter(user_id=user_id).filter(groups__name__in=groups).count() > 0


def get_user_id(request):
    token = request.META.get('HTTP_X_CSRF_TOKEN')
    if token is None:
        return None

    try:
        userToken = Token.objects.get(key=token)
    except Token.DoesNotExist:
        return None

    request.id = userToken.user_id
    request.user = User.objects.get(user_id=userToken.user_id)

    return userToken.user_id


def is_admin_user(request):
    """ Checks if user is in dev or HS """
    user_id = get_user_id(request)

    if user_id is None:
        return False

    return User.objects.filter(user_id=user_id).filter(groups__name__in=['DevKom', 'HS']).count() > 0 \
        or request.user.is_staff
