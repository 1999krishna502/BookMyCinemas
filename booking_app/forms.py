from django import forms
from .models import *


class Signup_forms(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(max_length=30)
    confirm_password = forms.CharField(max_length=30)

class login_forms(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=30)

class BookingForm(forms.Form):
    email = forms.EmailField()
    num_tickets = forms.IntegerField(min_value=1)
    showtime_id = forms.IntegerField()

class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = ['movie', 'theater', 'time']