from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending
import requests as req


# Create your views here.

def signup(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        user_pwd = request.POST.get("password")

        try:
            user = User.objects.filter(username=user_name).first()
            if user:
                return render(request, "signup.html", {"form": SignUpForm(),
                                                       "message": "Username already exists"})
            else:
                user = User.objects.create(username=user_name, password=make_password(user_pwd))
                login(request, user)
                return HttpResponseRedirect(reverse("index"))

        except User.DoesNotExist:
            return render(request, "signup.html", {"form": SignUpForm()})

    return render(request, "signup.html", {"form": SignUpForm()})


def index(request):
    return render(request, "index.html")




# Define a view function named 'songs' that takes an HTTP request object as its parameter
def songs(request):
    # Create a dictionary with a single key "songs" that contains a list of song dictionaries
    songs = {"songs":[
        {
            "id":1,
            "title":"duis faucibus accumsan odio curabitur convallis",
            # The lyrics field uses parentheses for implicit string concatenation across multiple lines (no + operator needed)
            "lyrics":("Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. " 
                      "Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis."
                      )
        }
    ]}
    # Call render() with: the request object, template path, and context dictionary
    # - note that songs["songs"] extracts the list from the outer dictionary before passing it to the template
    return render(request, "songs.html", {"songs":songs["songs"]})

def photos(request):
    photos = [{
    "id": 1,
    "pic_url": "http://dummyimage.com/136x100.png/5fa2dd/ffffff",
    "event_country": "United States",
    "event_state": "District of Columbia",
    "event_city": "Washington",
    "event_date": "11/16/2022"
}]

    return render(request, "photos.html", {"photos": photos})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
                user=User.objects.filter(username=username).first()
                if user and user.check_password(password):
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
        except User.DoesNotExist:
            return render (request, "login.html", {"form": LoginForm(), "message": "Invalid Credentials"})
    return render(request, "login.html", {"form": LoginForm()})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def concerts(request):
    user = request.user
    if user.is_authenticated:
        list_of_concerts = []
        concert_objects = Concert.objects.all()
        for concert in concert_objects:
            try:
                status = concert.attendee.filter(user=user.first().attending)
            except:
                status = "-"
            list_of_concerts.append({"concert_details": concert, "status": status})
        return render(request, "concerts.html", {"concerts": list_of_concerts})
    else:
        return HttpResponseRedirect(reverse("login"))



def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = Concert.objects.get(pk=id)
        try:
            status = obj.attendee.filter(user=request.user).first().attending
        except:
            status = "-"
        return render(request, "concert_detail.html", {
            "concert_details": obj, "status": status, "attending_choices": ConcertAttending.AttendingChoices.choices
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    pass


def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")
            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id, user=request.user).first()
            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(concert_id=concert_id,
                                                user=request.user,
                                                attending=attendee_status)

        return HttpResponseRedirect(reverse("concerts"))
    else:
        return HttpResponseRedirect(reverse("index"))
