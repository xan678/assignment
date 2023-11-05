from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ShortURL
from .serializers import ShortURLSerializer
from .shortcode import generate_unique_short_code
from .permissions import RetrieveOrReadOnly

class ShortURLViewSet(viewsets.ModelViewSet):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    permission_classes = [RetrieveOrReadOnly]

    def create(self, request):
        original_url = request.data.get('original_url')
        expiry = request.data.get('expiry')
        one_time_use = request.data.get('one_time_use')

        try:
            expiry = int(expiry)
        except ValueError:
            return Response({'error' : 'Invalid expiry value'}, status=status.HTTP_404_NOT_FOUND)
        
        expiry_datetime = datetime.now() + timedelta(seconds=expiry)

        short_code = generate_unique_short_code()

        uses_left = 1 if one_time_use else 100

        short_url = ShortURL(
            user = request.user,
            original_url = original_url,
            short_code = short_code,
            expiry_time = expiry_datetime,
            uses_left = uses_left,
            status = 'ACT'
        )

        short_url.save()

        return Response({'short_url' : short_url.short_code}, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def retrieve(self, request, pk=None):
        try:
            short_url = ShortURL.objects.get(short_code= pk, status='ACT')
        except ShortURL.DoesNotExist:
            return Response({'error': 'Short URL not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if short_url.expiry_time < datetime.now().date() or short_url.uses_left < 1: 
            short_url.status = 'EXP'
            short_url.save()
            return Response({'error': 'Short URL has expired'}, status=status.HTTP_404_NOT_FOUND)
        
        count = short_url.uses_left - 1
        short_url.uses_left = count
        short_url.save()
        print(short_url.uses_left)

        # short_url.objects.update(uses_left=count)

        return redirect(short_url.original_url)
    
    def list(self, request):
        queryset = ShortURL.objects.filter(user = request.user)
        serializer = ShortURLSerializer(queryset, many=True)

        return Response(serializer.data)
    
    def update(self, request):
        
        short_code = request.data.get('short_code')
        extend = request.data.get('extend')

        try:
            short_url = ShortURL.objects.get(short_code= short_code)
        except ShortURL.DoesNotExist:
            return Response({'error' : 'Invalid short code'}, status=status.HTTP_404_NOT_FOUND)

        short_url.uses_left = short_url.uses_left + int(extend)
        short_url.status = 'ACT'

        short_url.save()
        
        return Response({'short_url' : short_code, 'uses_left': short_url.uses_left}, status=status.HTTP_200_OK)
