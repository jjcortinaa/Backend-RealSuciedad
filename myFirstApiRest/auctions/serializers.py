from rest_framework import serializers
from .models import Auction, Category
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema_field


class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AuctionListCreateSerializer(serializers.ModelSerializer):
    isOpen = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Auction
        fields = '__all__'

    def validate_closing_date(self, value):
        if value <= timezone.now() + timedelta(days=15):
            raise serializers.ValidationError("Closing date must be greater than now.")
        return value
    
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        if obj.closed_at is None:
            return True
        return obj.closed_at > timezone.now()
    
class AuctionDetailSerializer(serializers.ModelSerializer):
    isOpen = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Auction
        fields = ['title', 'description', 'price', 'category', 'isOpen']
        read_only_fields = ['created_at', 'updated_at', 'id']

    def validate_closing_date(self, value):
        if value <= timezone.now() + timedelta(days=15):
            raise serializers.ValidationError("Closing date must be greater than now.")
        return value
    
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        if obj.closed_at is None:
            return True
        return obj.closed_at > timezone.now()
    