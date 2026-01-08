from rest_framework import serializers
from .models import PalabraModo1, PalabraModo2

class PalabraModo1Serializer(serializers.ModelSerializer):
    class Meta:
        model = PalabraModo1
        fields = '__all__'

class PalabraModo2Serializer(serializers.ModelSerializer):
    class Meta:
        model = PalabraModo2
        fields = '__all__'
