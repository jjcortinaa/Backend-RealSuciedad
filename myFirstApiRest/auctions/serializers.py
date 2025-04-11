from rest_framework import serializers
from django.utils import timezone
from .models import Category, Auction
from datetime import timedelta
from drf_spectacular.utils import extend_schema_field
from django.utils.dateparse import parse_datetime


class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AuctionListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser un número positivo.')
        return value

    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError('El stock debe ser un número natural positivo.')
        return value

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError('La valoración debe ser un número entre 1 y 5.')
        return value

    def validate_closing_date(self, value):
        creation_date_str = self.initial_data.get('creation_date')

        if creation_date_str:
            creation_date = parse_datetime(creation_date_str)
        else:
            creation_date = timezone.now()

        if creation_date is None:
            raise serializers.ValidationError('La fecha de creación no es válida.')

        if value <= creation_date:
            raise serializers.ValidationError('La fecha de cierre no puede ser menor o igual a la fecha de creación.')

        if value < creation_date + timedelta(days=15):
            raise serializers.ValidationError('La fecha de cierre debe ser al menos 15 días después de la fecha de creación.')

        return value
class AuctionDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser un número positivo.')
        return value

    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError('El stock debe ser un número natural positivo.')
        return value

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError('La valoración debe ser un número entre 1 y 5.')
        return value

    def validate_closing_date(self, value):
        creation_date = self.instance.creation_date  

        if value <= creation_date:
            raise serializers.ValidationError('La fecha de cierre no puede ser menor o igual a la fecha de creación.')

        if value < creation_date + timedelta(days=15):
            raise serializers.ValidationError('La fecha de cierre debe ser al menos 15 días después de la fecha de creación.')

        return value
