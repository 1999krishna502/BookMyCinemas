from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


# Create your models here.

class signup_model(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    balance=models.IntegerField()

class deposit_model(models.Model):
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    uid = models.IntegerField()

class withdraw_model(models.Model):
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    uid = models.IntegerField()

class Theater(models.Model):
    theater_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=30)
    description = models.CharField(max_length=255)


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    time = models.CharField(max_length=10)
    seats_available = models.IntegerField(default=100)

class Booking(models.Model):

    signup_model=models.ForeignKey(signup_model, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    num_tickets = models.IntegerField()
    amount=models.IntegerField()


    def clean(self):
        # Custom clean method for additional validation
        if self.num_tickets > self.showtime.seats_available:
            raise ValidationError("Not enough seats available")

