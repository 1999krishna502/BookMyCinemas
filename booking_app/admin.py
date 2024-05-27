from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(signup_model)
admin.site.register(deposit_model)
admin.site.register(withdraw_model)
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Showtime)
admin.site.register(Booking)