from rest_framework import serializers
from .models import Auction, Category, Bid, Rating
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

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closed_at is None or obj.closed_at > timezone.now()

    def validate(self, data):
        # Obtener la fecha de creación (automáticamente añadida si no se pasa explícitamente)
        creation_date = self.instance.created_at if self.instance else timezone.now()

        closing_date = data.get('closed_at')
        if closing_date:
            if closing_date <= creation_date:
                raise serializers.ValidationError({
                    'closed_at': 'The closing date cannot be less than or equal to the creation date.'
                })
            if closing_date < creation_date + timedelta(days=15):
                raise serializers.ValidationError({
                    'closed_at': 'The closing date must be at least 15 days after the creation date.'
                })
        else:
            raise serializers.ValidationError({
                'closed_at': 'This field is required.'
            })

        return data
    
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
        
        if bid:
            if data.get('price', bid.price) <= bid.price:
                raise serializers.ValidationError("La cantidad de la puja debe ser mayor a la puja anterior.")
        
        if 'price' in data and data['price'] > auction.price:
            auction.price = data['price']
            auction.save()  

        return data
    
class BidListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
    
    def validate(self, data):
        bid = self.instance
        auction = data.get("auction")

        if not auction :
            raise serializers.ValidationError("Debes proporcionar una subasta válida.")
            
        if auction.closed_at and auction.closed_at <= timezone.now():
            raise serializers.ValidationError("La subasta está cerrada. No puedes realizar una puja.")

        if bid:
            if data.get('price', bid.price) <= bid.price:
                raise serializers.ValidationError("La cantidad de la puja debe ser mayor a la puja anterior.")

        if 'price' in data and data['price'] > auction.price:
            auction.price = data['price']
            auction.save()  

        return data

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'auction', 'value']

    def create(self, validated_data):
        # El user se asigna automáticamente en la vista
        return Rating.objects.create(**validated_data, user=self.context['request'].user)

    