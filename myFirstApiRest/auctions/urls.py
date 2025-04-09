from django.urls import path
from .views import CategoryListCreate, CategoryRetrieveUpdateDestroy, AuctionListCreate, AuctionRetrieveUpdateDestroy, AuctionSearch

app_name="auctions"
urlpatterns = [
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('<str:texto>/', AuctionListCreate.as_view(), name='auction-list-create'),
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),
    path('search/', AuctionSearch.as_view(), name='auction-search')
]