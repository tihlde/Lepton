from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.response import Response

from ..models import User
from ..permissions import IsMember, IsDev
from ..serializers import UserSerializer, UserMemberSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint to display one user """
    serializer_class = UserSerializer
    permission_classes = [IsMember, ]
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def get_permissions(self):
        # Your logic should be all here
        if self.request.method == 'POST':
            self.permission_classes = [IsDev, ]
        else:
            self.permission_classes = [IsMember, ]
        return super(UserViewSet, self).get_permissions()

    def get_object(self):
        """Returns one application"""
        id = self.request.info['uid'][0]

        try:
            User.objects.get(user_id = id)
        except User.DoesNotExist:
            new_data = {
                'user_id': id,
                'first_name': self.request.info['givenname'][0],
                'last_name': self.request.info['sn'][0],
                'email': self.request.info['mail'][0]
            }
            serializer = UserSerializer(data=new_data)
            if serializer.is_valid():
                serializer.save()
        return User.objects.get(user_id=id)

    def list(self, request):
        if IsMember.isDev(self, request):
            serializer = UserSerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        return Response({'detail': _('Not authenticated to see all users')}, status=400)

    def perform_create(self, serializer):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()

    def update(self, request, pk, *args, **kwargs):
        """ Updates fields passed in request """
        try:
            self.check_object_permissions(self.request, User.objects.get(user_id=pk))
            if self.request.info['uid'][0] == pk:
                serializer = UserMemberSerializer(User.objects.get(user_id=pk), context={'request': request}, many=False, data=request.data)
                if serializer.is_valid():
                    self.perform_update(serializer)
                    return Response({'detail': _('User successfully updated.')})
                else:
                    return Response({'detail': _('Could not perform user update')}, status=400)
            else:
                return Response({'detail': _('Not authenticated to perform user update')}, status=400)
        except ObjectDoesNotExist:
            return Response({'detail': 'Could not find user'}, status=400)
