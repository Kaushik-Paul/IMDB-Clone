from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=20)
    about = models.CharField(max_length=100)
    url = models.URLField(max_length=100)

    def __str__(self):
        return self.name + " | " + self.url


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    # Many-to-One relationship
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    is_active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " | " + str(self.avg_rating) + " | " + self.platform.name


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title + " | " + self.review_user.username
