from django.db import models
from user_app.models import UserModel
from book_app.models import BookModel

# Create your models here.


class Cart(models.Model):

    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book_id = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.FloatField()
    total_price = models.FloatField()

    def __str__(self):
        return self.user_id

