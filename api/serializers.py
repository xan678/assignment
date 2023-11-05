from rest_framework import serializers
from .models import ShortURL, URLUsageLog

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = '__all__'

class URLUsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLUsageLog
        fields = '__all__'
        
