from rest_framework import serializers
from .models import User, Service, ServiceRequest, Payment, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'location', 'average_rating', 'profile_photo']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'is_active']


class ServiceRequestSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)
    provider_name = serializers.CharField(source='provider.username', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = ['id', 'client_name', 'provider_name', 'service_name', 'amount', 'status', 'message', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'method', 'status', 'paid_at', 'transaction_id']


class RatingSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'client_name', 'rating', 'review', 'created_at']