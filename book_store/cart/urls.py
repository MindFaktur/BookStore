from django.urls import path
from .views import AddToCart

urlpatterns = [
    path('addtocart/', AddToCart.as_view(), name='add to cart'),
]