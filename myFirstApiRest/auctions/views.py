from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import Category, Auction
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer
# Create your views here.



class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer
class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
class AuctionListCreate(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListCreateSerializer

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

class AuctionSearch(generics.ListAPIView):
    serializer_class = AuctionListCreateSerializer

    def get_queryset(self):
        queryset = Auction.objects.all()

        # Filtro por texto
        texto = self.request.query_params.get('texto', None)
        if texto:
            queryset = queryset.filter(title__icontains=texto) | queryset.filter(description__icontains=texto)

        # Filtro por categoría
        category_id = self.request.query_params.get('categoria', None)
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        # Filtro por rango de precio
        precio_min = self.request.query_params.get('precioMin', None)
        precio_max = self.request.query_params.get('precioMax', None)
        if precio_min:
            queryset = queryset.filter(price__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(price__lte=precio_max)

        return queryset