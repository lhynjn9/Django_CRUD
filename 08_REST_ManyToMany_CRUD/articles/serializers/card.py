# 유지보수 및 관리를 위해 분리

from rest_framework import serializers
from ..models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'