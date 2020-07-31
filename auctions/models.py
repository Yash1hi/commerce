from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=512)
    category = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    image = models.CharField(max_length=512, blank=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchers")
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", default=None)

    def __str__(self):
        return f"{self.name} ({self.category}): {self.description} Image Link: {self.image}. Is being watched by: {self.watchers}"

class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bidder")
    bid = models.FloatField()

    def __str__(self):
        return f"For {self.listing_id}, the bid is {self.bid} placed by {self.bidder}"

class Comment(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Commenter")
    comment = models.CharField(max_length=512)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.listing_id} Comment: {self.comment} was made by user {self.user} on {self.date}"

