from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from facilities.models import Instalacion, UCEntity
from rest_framework import viewsets
from .serializers import InstalacionSerializer, UCEntitySerializer

class InstalacionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Instalacion.objects.all().order_by('id')
    serializer_class = InstalacionSerializer


class UCEntityViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UCEntity.objects.all().order_by('instalacion_id')
    serializer_class = UCEntitySerializer