from django.shortcuts import render
from rest_framework import generics
from rest_framework import serializers
from django.db.models import Q
from rest_framework.response import Response
from .models import Category, Auction, Bid, Rating
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidDetailSerializer, BidListCreateSerializer, RatingSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin
from rest_framework.exceptions import NotFound
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
    permission_classes = [IsOwnerOrAdmin] 
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

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
    
class UserAuctionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # Obtener las subastas del usuario autenticado
        user_auctions = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(user_auctions, many=True)
        return Response(serializer.data)
    
class BidListCreate(generics.ListCreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidListCreateSerializer

    def perform_create(self, serializer):
        # Obtener el auction_id desde el cuerpo de la solicitud
        auction_id = self.request.data.get('auction')
        
        # Verificar que la subasta existe
        try:
            auction = Auction.objects.get(id=auction_id)
        except Auction.DoesNotExist:
            raise serializers.ValidationError("Subasta no válida o no encontrada.")

        # Guardar la puja y asociarla con la subasta correcta
        serializer.save(auction=auction)

        return Response({
            "id": auction.id,
            "auction_price": auction.price,
            "bid": serializer.data
        })

class BidDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BidDetailSerializer
        return BidListCreateSerializer

    def get_queryset(self):
        auction_id = self.kwargs.get('id_auction')
        bid_id = self.kwargs.get('pk')  

        return Bid.objects.filter(id=bid_id, auction_id=auction_id)

    def perform_update(self, serializer):
        auction_id = self.kwargs.get('id_auction')
        bid_id = self.kwargs.get('pk')
        
        # Intentar obtener la subasta
        try:
            auction = Auction.objects.get(id=auction_id)
        except Auction.DoesNotExist:
            raise NotFound("La subasta con el ID especificado no existe.")
        
        # Actualizar la puja
        bid = serializer.save(auction=auction)
        return bid
    
class AuctionBidListCreate(generics.ListCreateAPIView):
    serializer_class = BidListCreateSerializer

    def get_queryset(self):
        auction_id = self.kwargs.get('auction_id')
        return Bid.objects.filter(auction__id=auction_id)

    def perform_create(self, serializer):
        auction_id = self.kwargs.get('auction_id')
        auction = Auction.objects.get(id=auction_id)
        serializer.save(auction=auction)


class RatingCreateUpdateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        auction = serializer.validated_data['auction']
        value = serializer.validated_data['value']
        user = self.request.user

        # Si ya existe, actualiza el rating
        existing_rating = Rating.objects.filter(auction=auction, user=user).first()
        if existing_rating:
            existing_rating.value = value
            existing_rating.save()
        else:
            serializer.save(user=user)

class RatingDeleteView(generics.DestroyAPIView):
    queryset = Rating.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        rating = super().get_object()
        if rating.user != self.request.user:
            raise ValidationError("No puedes eliminar una valoración que no es tuya.")
        return rating
    
class RatingListView(generics.ListAPIView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        # Ordena los resultados, por ejemplo, por la fecha de creación (suponiendo que la tengas en el modelo)
        return Rating.objects.filter(auction_id=auction_id).order_by('id')  # O el campo que desees ordenar
