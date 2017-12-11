from __future__ import unicode_literals
from django.shortcuts import render, redirect
from ..login.models import User
from .models import Travel
from django.contrib.messages import error
from django.contrib import messages
import datetime

def index(request):
    """
    Sessions have been created in my index.html page which then pulls the info that I enter into my database to show up on my webpage.
    """
    if "user_id" not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    alltravels = Travel.objects.filter(travels=user)
    othertravels = Travel.objects.exclude(travels=user)

    context = {
        "users": user,
        "alltravels": alltravels,
        "othertravels": othertravels,
    }
    return render(request, 'travel/index.html', context)

def new(request):
    """
    Takes the user to a new page where they can add a new travel to their trip schedule.
    """
    if "user_id" not in request.session:
        return redirect('/')
    return render(request, 'travel/create.html')

def create(request):
    """
    Create allows the user to add an new trip which immediately goes to the database in the correct table fields based off of my model. Validations are set up to mae sure that none of the fields are left empty and trip dates are in the future. Past dates are also validated to prevent the user from using a past date before the start date. Add is my one to many relationship which pulls that particular users trips they create from the database. 
    """
    result = Travel.objects.validate(request.POST)
    print result, 'errors'
    if len(result) > 0:
        for err in result:   
            print err
            messages.error(request, err)
        return redirect('/travel/new') # ends the function and replaces the caller with itself

    people=User.objects.get(id=request.session['user_id'])
    newtravel = Travel.objects.create(
        destination=request.POST['destination'],
        travel_start=request.POST['travel_start'],
        travel_end=request.POST['travel_end'],
        plan=request.POST['plan'],
        add=people, # One to many relationship that adds the new plan to the correct name 
    )
    newtravel.travels.add(people) 
    return redirect('/travel')

def view(request, number):
    """
    This data pulls up on the destination.html page which shows the trip and other users that have joined as well. 
    """
    if "user_id" not in request.session:
        return redirect('/')
    
    context = {
        "travel": Travel.objects.get(id=number),
        "travelers": User.objects.filter(travelled_by=number).exclude(id=request.session['user_id'])
    }
    return render(request, 'travel/destination.html', context)

def home(request):
    if "user_id" not in request.session:
        return redirect('/')
    return redirect('/travel')
 
def logout(request):
    """
    Flush clears the session once the user logs out preventing from constantaly having to refresh the page to clean out the info. 
    """
    request.session.flush()
    return redirect('/')

def join(request, number):
    """
    Allows a user to join other travels with other users.
    """
    user = User.objects.get(id=request.session['user_id'])
    addtravel = Travel.objects.get(id=number)
    addtravel.travels.add(user)
    return redirect('/travel')

def remove(request, number):
    """
    Remove is setting up my many to many relationship with removing a particular trip from a users schedule. This is not required on the exam I just wanted this option to remove a user from a trip they joined as they most likely can't make it anymore!
    """
    thistravel = Travel.objects.get(id=number)
    thisuser = User.objects.get(id=request.session['user_id'])
    thistravel.travels.remove(thisuser)
    return redirect('/travel')  

def delete(request, number):
    """
    Allows the user who's logged in to delete a trip that they created from the system. This is not part of the exam but I wanted to add it in so I have the option to delete a planned trip in case I messed up on the location or changed my mind. 
    """
    Travel.objects.get(id=number).delete()
    return redirect('/travel')