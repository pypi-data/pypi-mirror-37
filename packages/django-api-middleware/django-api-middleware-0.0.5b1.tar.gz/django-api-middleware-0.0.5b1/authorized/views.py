"""
================
MIDDLEWARE VIEWS
================
"""
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from authorized.models import Applications
from authorized.serializers import AuthorizedAppSerializer
# Create your views here.


class MockThirdPartyViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin):
    queryset = Applications.objects.all()
    serializer_class = AuthorizedAppSerializer

    def create(self, request, *args, **kwargs):
        return Response({'message': 'Mock third party created successfully'}, status=status.HTTP_201_CREATED)


class MockNonThirdPartyViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin):
    queryset = Applications.objects.all()
    serializer_class = AuthorizedAppSerializer

    def create(self, request, *args, **kwargs):
        return Response({'message': 'Mock non third party created successfully'}, status=status.HTTP_201_CREATED)