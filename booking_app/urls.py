from django.conf import settings
from django.urls import path

from django.conf.urls.static import static
from . import views
from .views import *

urlpatterns=[

    path('signup/',Signup),
    path('login/',login),

    path('logout/',logout_views),

    path('add_money/<int:id>',add_money),
    path('add_money_success/',add_money_success),
    path('add_money_display/',add_money_display),

    path('withdraw/<int:id>',withdraw),
    path('withdraw_success/',withdraw_success),
    path('withdraw_display/',withdraw_display),

    path('balance/<int:id>',checkbalance),
    path('balance_display/',balance_display),



    path('profile/', views.profile, name='profile'),
    path('theater_details/',theater_details),
    path('showtimes/', views.show_details, name='showtime_details'),
    path('book_tickets/', views.book_tickets, name='book_tickets'),
    path('payment/', views.payment, name='payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('booking_details/', views.booking_details_api, name='booking_details_api'),





    path('movies/', views.MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),

    # path('book_tickets/', book_tickets),



    # path('showtimes/', showtime_details, name='showtime_detail'),
    path('cancel_booking/', cancel_booking, name='cancel_booking'),




    path('api/theaters/', TheaterListView.as_view(), name='theater-list'),
    path('api/theaters/<int:pk>/', TheaterDetailView.as_view(), name='theater-detail'),
    path('api/movies/', MovieListView.as_view(), name='movie-list'),
    path('api/movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('api/showtimes/', ShowtimeListCreateView.as_view(), name='showtime-list'),
    path('api/showtimes/<int:pk>/', ShowtimeRetrieveUpdateDestroyView.as_view(), name='showtime-detail'),
    # path('create_showtime_api/', create_showtime_api, name='create_showtime_api'),

    path('api/bookings/', BookingListCreateAPIView.as_view(), name='booking-list'),
    path('api/bookings/<int:pk>/', BookingRetrieveUpdateDestroyAPIView.as_view(), name='booking-detail'),

    path('api/booking_details/', booking_details_api, name='booking-details-api'),
    # path('booking_details/', booking_details, name='booking-details'),



]