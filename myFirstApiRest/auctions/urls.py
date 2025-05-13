from django.urls import path
from .views import CategoryListCreate, CategoryRetrieveUpdateDestroy, AuctionListCreate, AuctionDetail, AuctionSearch, UserAuctionListView, BidDetail, AuctionBidListCreate, RatingListCreateView, RatingRetrieveUpdateDestroyView

app_name="auctions"
urlpatterns = [
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('search/', AuctionSearch.as_view(), name='auction-search'),
    path('<int:pk>/', AuctionDetail.as_view(), name='auction-detail'),
    path('users/', UserAuctionListView.as_view(), name='action-from-users'),
    # path('<int:id_auction>/bids/', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:id_auction>/bids/<int:pk>', BidDetail.as_view(), name='bid-detail'),
    path('<int:auction_id>/bids/', AuctionBidListCreate.as_view(), name='auction-bid-list-create'),
    path('ratings/', RatingListCreateView.as_view(), name='rating-create-update'),
    path('ratings/<int:pk>/', RatingRetrieveUpdateDestroyView.as_view(), name='rating-delete'),
]