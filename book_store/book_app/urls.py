from django.urls import path
from .views import AddBook

urlpatterns = [
    path('books/', AddBook.as_view(), name='All book operations'),

]
