from django.urls import path
from .views import CategoryListCreate, CategoryRetrieveUpdateDestroy, AuctionListCreate, AuctionDetail, AuctionSearch, UserAuctionListView, BidDetail, BidListCreate

app_name="auctions"
urlpatterns = [
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('search/', AuctionSearch.as_view(), name='auction-search'),
    path('<int:pk>/', AuctionDetail.as_view(), name='auction-detail'),
    path('users/', UserAuctionListView.as_view(), name='action-from-users'),
    path('<int:id_auction>/bids/', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:id_auction>/bids/<int:pk>', BidDetail.as_view(), name='bid-detail'),
]