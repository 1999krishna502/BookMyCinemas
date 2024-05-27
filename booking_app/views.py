

from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from rest_framework import generics
from django.contrib.auth import logout

from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BaseAuthentication , TokenAuthentication
from rest_framework.permissions import AllowAny , IsAdminUser


from .serializers import *
from .forms import *
from .models import *
# Create your views here.

def Signup(request):
    if request.method=="POST":
        a=Signup_forms(request.POST)
        if a.is_valid():
            n=a.cleaned_data['name']
            em=a.cleaned_data['email']
            psw=a.cleaned_data['password']
            cpsw=a.cleaned_data['confirm_password']
            a=signup_model.objects.all()
            for i in a:
                if (em == i.email):
                    return HttpResponse('allready exist')
            else:
                if cpsw == psw:
                    b = signup_model(name=n, email=em,password=psw,balance=0)
                    b.save()
                    return redirect(login)
                else:
                    return HttpResponse("password doesn't match! ")
        else:
            return HttpResponse('registration failed invalid datas!')
    return render(request,'signup.html')


def login(request):
    if request.method == "POST":
        a = login_forms(request.POST)
        if a.is_valid():
            em = a.cleaned_data['email']
            psw = a.cleaned_data['password']
            b = signup_model.objects.all()
            for i in b:
                if i.email == em and i.password == psw:
                    request.session['id']=i.id
                    return redirect(profile)
            else:
                return HttpResponse('login failed')
    return render(request,'login.html')

def logout_views(request):
    logout(request)
    return redirect(Signup)


# **************************************************************************************************#

def show_details(request):
    showtimes = Showtime.objects.all()
    context = {'showtimes': showtimes}
    return render(request, 'show_details.html', context)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Booking, Showtime, signup_model
from .forms import BookingForm

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Booking, Showtime, signup_model
from .forms import BookingForm

TICKET_PRICE = 140
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Showtime, Booking
from .forms import BookingForm  # Assuming BookingForm is defined in forms.py






TICKET_PRICE = 140

@csrf_protect
def book_tickets(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['email'] = email
            num_tickets = form.cleaned_data['num_tickets']
            showtime_id = form.cleaned_data['showtime_id']

            showtime = get_object_or_404(Showtime, pk=showtime_id)


            if num_tickets > showtime.seats_available:
                return JsonResponse({'error': 'Not enough seats available'}, status=400)

            user = get_object_or_404(signup_model, email=email)  # Assuming signup_model is your user model


            # Calculate the amount
            amount = num_tickets * TICKET_PRICE
            request.session['amount'] = amount

            # Create the booking
            booking = Booking.objects.create(
                signup_model=user,
                showtime=showtime,
                num_tickets=num_tickets,
                amount=amount
            )
            booking.save()

            # Update seats available
            showtime.seats_available -= num_tickets
            showtime.save()

            return redirect(payment)

        return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)

    else:
        form = BookingForm()
        showtimes = Showtime.objects.all()
        return render(request, 'book_tickets.html', {'form': form, 'showtimes': showtimes, 'ticket_price': TICKET_PRICE})





def booking_details_api(request):
    user_id = request.session.get('id')
    am = request.POST.get('amount')
    request.session['am'] = am

    if not user_id:
        return JsonResponse({'message': 'User not authenticated'}, status=403)

    try:
        user = signup_model.objects.get(id=user_id)
    except signup_model.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)

    bookings = Booking.objects.filter(signup_model=user)

    if not bookings.exists():
        return JsonResponse({'message': 'No bookings found'}, status=404)

    booking_details = []
    for booking in bookings:
        showtime = booking.showtime
        movie = showtime.movie
        theater = showtime.theater

        booking_details.append({
            'user_email': user.email,
            'user_name': user.name,
            'movie': movie.title,
            'theater': theater.theater_name,
            'location': theater.location,
            'time': showtime.time,
            'num_seats': booking.num_tickets,
            'amount': booking.amount,

        })


    return render(request, 'booking_details.html', {'bookings': booking_details})



def payment(request):
    id = request.session['id']
    a = signup_model.objects.get(id=id)
    if request.method == 'POST':
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        request.session['am'] = amount


        if email == a.email:
            if a.balance >= int(amount):
                a.balance -= int(amount)
                a.save()
                withdraw_model.objects.create(amount=amount, uid=id)
                return redirect('payment_success')
            else:
                return HttpResponse('Insufficient balance.')
        else:
            return HttpResponse('Incorrect email.')
    return render(request, 'payment.html', {'a': a})


def payment_success(request):
    am = request.session.get('am')
    id = request.session.get('id')
    a = signup_model.objects.get(id=id)
    return render(request, "payment_success.html", {'am': am, 'a': a})


#cancel


def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = Booking.objects.filter(id=booking_id).first()
        if booking:
            booking.delete()
    bookings = Booking.objects.all()
    return render(request, 'booking_details.html', {'bookings': bookings})






def profile(request):
    id = request.session.get('id')
    a = signup_model.objects.get(id=id)
    movies = Movie.objects.all()
    serialized_movies = MovieSerializer(movies, many=True)
    context = {
        'movies': serialized_movies.data,
        'a': a
    }
    return render(request, 'profile.html', context)


def theater_details(request):
    # Fetch movie data from APIs (Assuming you have a function fetch_movies_from_api)
    movies = Movie.objects.all()

    # Get theater details
    theaters = Theater.objects.all()

    # Get available seats for each showtime
    showtimes = Showtime.objects.select_related('theater').all()

    context = {
        'movies': movies,
        'theaters': theaters,
        'showtimes': showtimes,
    }
    return render(request, 'theater_details.html', context)

#**********************************************************************************************************************#

def add_money(request,id):
    a = signup_model.objects.get(id=id)
    if request.method == 'POST':
        am = request.POST.get('amount')
        password = request.POST.get('password')
        request.session['am'] = am
        if password == a.password:
            a.balance += int(am)
            a.save()
            b = deposit_model(amount=am, uid=request.session['id'])
            b.save()
            return redirect(add_money_success)
        else:
            return HttpResponse('failed')
    return render(request, 'add_money.html')

def add_money_success(request):
    am=request.session['am']
    return render(request,'add_money_success.html',{'am':am})

def add_money_display(request):
    a=deposit_model.objects.all() #fetchall
    id=request.session['id']
    return render(request,'add_money_display.html',{'a':a,'id':id})


def withdraw(request,id):
    a = signup_model.objects.get(id=id)
    if request.method == 'POST':
        am = request.POST.get('amount')
        password = request.POST.get('password')
        request.session['am'] = am
        if password == a.password:
            if (a.balance >= int(am)):
                a.balance -= int(am)
                a.save()
                b = withdraw_model(amount=am, uid=request.session['id'])
                b.save()
                return redirect(withdraw_success)
            else:
                return HttpResponse('insufficient balance...')
        else:
            return HttpResponse('password incorrect..')
    return render(request, 'withdraw.html')

def withdraw_success(request):
    am=request.session['am']
    return render(request,'withdraw_success.html',{'am':am})

def withdraw_display(request):
    a=withdraw_model.objects.all() #fetchall
    id=request.session['id']
    return render(request,'withdraw_display.html',{'a':a,'id':id})

def checkbalance(request,id):
    a = signup_model.objects.get(id=id)
    if request.method == 'POST':
        request.session['email'] = a.email
        request.session['balance'] = a.balance
        password = request.POST.get('password')
        if password == a.password:
            return redirect(balance_display)
        else:
            return HttpResponse('wrong password..')
    return render(request,'balance.html')

def balance_display(request):
    email = request.session['email']
    ba = request.session['balance']
    return render(request,'balance_display.html',{'balance':ba,'email':email})



#*********************************************************************************************************************#

class TheaterListView(generics.ListCreateAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

class TheaterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ShowtimeListCreateView(generics.ListCreateAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer

class ShowtimeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
#
class BookingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
















