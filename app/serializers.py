from rest_framework import serializers, pagination
from app.models import DailyPrice

class DailyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPrice
        fields = '__all__'
