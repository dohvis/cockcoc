from rest_framework import serializers
from .models import (
    Bar,
)


class BarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bar
        fields = ('pk', 'name', 'address', 'description', 'phone', 'lat', 'lng', 'image',)
