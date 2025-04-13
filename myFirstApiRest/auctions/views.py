from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidDetailSerializer, BidListCreateSerializer
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


class AuctionSearch(generics.ListAPIView):
    serializer_class = AuctionListCreateSerializer
    queryset = Auction.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()
        texto = self.request.query_params.get('description', '')
        category_name = self.request.query_params.get('category', '')
        precio_min = self.request.query_params.get('priceMin', None)
        precio_max = self.request.query_params.get('priceMax', None)

        filters = Q()
        if texto:
            filters &= Q(title__icontains=texto) | Q(description__icontains=texto)
        if category_name:
            filters &= Q(category__name__iexact=category_name)
        if precio_min:
            filters &= Q(price__gte=precio_min)
        if precio_max:
            filters &= Q(price__lte=precio_max)

        return queryset.filter(filters)
    
class AuctionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "PUT":
            return AuctionDetailSerializer
        return AuctionListCreateSerializer
    
class BidListCreate(generics.ListCreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidListCreateSerializer

class BidDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bid.objects.all()
    def get_serializer_class(self):
        if self.request.method == "PUT":
            return BidDetailSerializer
        return BidListCreateSerializer