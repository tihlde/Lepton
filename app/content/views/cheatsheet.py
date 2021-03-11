from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from sentry_sdk import capture_exception

from app.common.drive_handler import upload_and_replace_url_with_cloud_link
from app.common.enums import AppModel, UserClass, UserStudy
from app.common.pagination import BasePagination
from app.common.perm import BasicViewPermission
from app.common.permissions import is_admin_user
from app.content.filters import CheatsheetFilter
from app.content.models import Cheatsheet
from app.content.serializers import CheatsheetSerializer


class CheatsheetViewSet(viewsets.ModelViewSet):
    serializer_class = CheatsheetSerializer
    permission_classes = [BasicViewPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    queryset = Cheatsheet.objects.all()
    pagination_class = BasePagination
    filterset_class = CheatsheetFilter
    search_fields = ["course", "title", "creator"]

    def get_object(self):
        if "pk" not in self.kwargs:
            return self.filter_queryset(self.queryset).filter(
                grade=UserClass(int(self.kwargs["grade"])),
                study=UserStudy[self.kwargs["study"]],
            )

        return super().get_object()

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return CheatsheetFilter(self.request.GET, queryset=queryset).qs

    def list(self, request, *args, **kwargs):
        """Return a list of cheatsheets filtered by UserClass and UserStudy"""
        try:
            cheatsheet = self.get_object()
            page = self.paginate_queryset(cheatsheet)
            if page is not None:
                serializer = CheatsheetSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = CheatsheetSerializer(
                cheatsheet, context={"request": request}, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cheatsheet.DoesNotExist as cheatsheet_not_exist:
            capture_exception(cheatsheet_not_exist)
            return Response(
                {"detail": "Kokeboken eksisterer ikke"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def create(self, request, *args, **kwargs):
        """Creates a new cheatsheet """
        upload_and_replace_url_with_cloud_link(request, AppModel.EVENT)
        serializer = CheatsheetSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Du har ikke tillatelse til å lage en oppskrift"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def update(self, request, *args, **kwargs):
        """Updates a cheatsheet retrieved by UserClass and UserStudy and pk"""
        try:
            upload_and_replace_url_with_cloud_link(request, AppModel.CHEATSHEET)
            cheatsheet = self.get_object()
            serializer = CheatsheetSerializer(cheatsheet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Cheatsheet.DoesNotExist as cheatsheet_not_exist:
            capture_exception(cheatsheet_not_exist)
            return Response(
                {"details": "Oppskriften ble ikke funnet"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def destroy(self, request, *args, **kwargs):
        """Deletes a cheatsheet retrieved by UserClass and UserStudy"""
        try:
            cheatsheet = self.get_object()
            if is_admin_user(request):
                super().destroy(cheatsheet)
                return Response(
                    {"detail": "Oppskriften har blitt slettet"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": "Du har ikke riktig tilatelser for å slette en oppskrift"},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Cheatsheet.DoesNotExist as cheatsheet_not_exist:
            capture_exception(cheatsheet_not_exist)
            return Response(
                {"details": "Oppskriften ble ikke funnet"},
                status=status.HTTP_404_NOT_FOUND,
            )
