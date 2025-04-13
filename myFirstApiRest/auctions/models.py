from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser 


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        ordering=('id',)

    def __str__(self):
        return self.name

class Auction(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    thumbnail = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(validators=[MinValueValidator(1)])
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)])
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='auctions',on_delete=models.CASCADE, default=0)
    auctioneer = models.ForeignKey(
        CustomUser,  # Referencia al modelo CustomUser
        related_name='auctions',  # Relación inversa en el modelo CustomUser
        on_delete=models.CASCADE,  # Si el usuario es eliminado, se eliminan las subastas
        null=True
    )
    def __str__(self):
        return self.title
    
class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    creation_date = models.DateTimeField(auto_now_add=True)
    bidder = models.CharField(max_length=255, null=True)

    class Meta:
        ordering=('-price','-creation_date')

    def __str__(self):
        return f"{self.bidder} - {self.price}€"