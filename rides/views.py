from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Ride, Booking
from .forms import RideForm, RegisterForm


def home(request):
    origin = request.GET.get('origin', '')
    destination = request.GET.get('destination', '')

    rides = Ride.objects.all()
    if origin:
        rides = rides.filter(origin__icontains=origin)
    if destination:
        rides = rides.filter(destination__icontains=destination)

    return render(request, 'rides/home.html', {
        'rides': rides,
        'origin_query': origin,
        'destination_query': destination
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добре дошли, {user.first_name}! Профилът ви беше създаден успешно.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'rides/register.html', {'form': form})


def ride_detail(request, pk):
    ride = get_object_or_404(Ride, pk=pk)
    has_booked = False
    if request.user.is_authenticated:
        has_booked = Booking.objects.filter(ride=ride, passenger=request.user).exists()

    return render(request, 'rides/ride_detail.html', {
        'ride': ride,
        'has_booked': has_booked
    })


@login_required
def book_ride(request, pk):
    ride = get_object_or_404(Ride, pk=pk)

    if ride.driver == request.user:
        messages.error(request, "Не можете да резервирате място в собственото си пътуване.")
        return redirect('ride_detail', pk=pk)

    if ride.available_seats <= 0:
        messages.error(request, "Няма останали свободни места.")
        return redirect('ride_detail', pk=pk)

    already_booked = Booking.objects.filter(ride=ride, passenger=request.user).exists()
    if already_booked:
        messages.error(request, "Вече сте резервирали място за това пътуване.")
        return redirect('ride_detail', pk=pk)

    Booking.objects.create(ride=ride, passenger=request.user, seats_booked=1)
    ride.available_seats -= 1
    ride.save()

    messages.success(request, "Успешно резервирахте място!")
    return redirect('ride_detail', pk=pk)


@login_required
def create_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user
            ride.save()
            return redirect('home')
    else:
        form = RideForm()

    return render(request, 'rides/create_ride.html', {'form': form})