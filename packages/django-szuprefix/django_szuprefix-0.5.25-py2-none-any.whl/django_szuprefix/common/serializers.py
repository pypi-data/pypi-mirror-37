# -*- coding:utf-8 -*- 

from rest_framework import serializers, viewsets, mixins, decorators
from . import models


class TempFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TempFile
        fields = ('url', 'name', 'file', 'id')

class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Image
        fields = ('url', 'name', 'file', 'id')
