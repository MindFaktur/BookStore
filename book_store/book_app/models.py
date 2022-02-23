from django.db import models

# Create your models here.


class BookModel(models.Model):
    book_name = models.CharField(unique=True, max_length=100)
    author_name = models.CharField(max_length=50)
    released_date = models.DateField()

    def __str__(self):
        return self.book_name

