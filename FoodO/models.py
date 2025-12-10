from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('restaurant', 'Restaurant'),
        ('ngo', 'NGO'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

class FoodDonation(models.Model):
    restaurant = models.CharField(max_length=200)
    food_name = models.CharField(max_length=200)
    food_type = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    location = models.CharField(max_length=300)
    phone = models.CharField(max_length=15)
    available_till = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_picked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.food_name} - {self.restaurant}"
    
    # NGO-Dashboard stats (manual control)
class DashboardStats(models.Model):
    food_rescued = models.IntegerField(default=0)
    people_fed = models.IntegerField(default=0)
    pickup_requests = models.IntegerField(default=0)


# Pickup request model
class PickupRequest(models.Model):
    donation = models.ForeignKey(FoodDonation, on_delete=models.CASCADE)
    ngo_name = models.CharField(max_length=100, default="NGO")
    status = models.CharField(max_length=30, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.donation.food_name}"
    
class RestaurantUser(models.Model):
     username = models.CharField(max_length=100)
     password = models.CharField(max_length=100)

     def __str__(self):
        return self.username
    
class NGOUser(models.Model):
     username = models.CharField(max_length=100)
     password = models.CharField(max_length=100)

     def __str__(self):
            return self.username
# Create your models here.
