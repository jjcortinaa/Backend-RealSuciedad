from rest_framework import serializers
from .models import Auction, Category, Bid
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

    
class BidDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['price']
        read_only_fields = ['id', 'bidder', 'creation_date', 'auction']
    
    def validate(self, data):
        bid = self.instance 
        auction = bid.auction 

        # Verificar si la subasta está cerrada
        if auction.closed_at:
            if auction.closed_at <= timezone.now():
                raise serializers.ValidationError("The auction is closed. You cannot update the bid.")

        return data
    
class BidListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
    
    def validate(self, data):
        bid = self.instance 
        auction = bid.auction 

        # Verificar si la subasta está cerrada
        if auction.closed_at:
            if auction.closed_at <= timezone.now():
                raise serializers.ValidationError("The auction is closed. You cannot update the bid.")
            
        if data.get('price', bid.price) <= bid.price:
            raise serializers.ValidationError("The bid amount must be greater than the previous highest bid.")

        return data

    