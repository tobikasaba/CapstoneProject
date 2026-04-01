from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse


from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending


def signup(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        user_pwd = request.POST.get("password")

        if not user_name or not user_pwd:
            return render(request, "signup.html", {
                "form": SignUpForm(),
                "message": "Username and password are required",
            })

        user = User.objects.filter(username=user_name).first()
        if user:
            return render(request, "signup.html", {
                "form": SignUpForm(),
                "message": "Username already exists",
            })

        # Use Django's auth helper so password handling follows the framework's user-creation flow.
        user = User.objects.create_user(username=user_name, password=user_pwd)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "signup.html", {"form": SignUpForm()})


def index(request):
    return render(request, "index.html")


def songs(request):
    songs = {"songs":[
        {
            "id":1,
            "title":"duis faucibus accumsan odio curabitur convallis",
            "lyrics":("Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. " 
                      "Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis."
                      )
        }
    ]}
    return render(request, "songs.html", {"songs": songs["songs"]})

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
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        return render(request, "login.html", {"form": LoginForm(), "message": "Invalid Credentials"})

    return render(request, "login.html", {"form": LoginForm()})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def concerts(request):
    user = request.user
    if user.is_authenticated:
        concerts_with_status = []
        concert_objects = Concert.objects.all()

        for concert in concert_objects:
            attendee = concert.attendee.filter(user=user).first()
            status = attendee.attending if attendee else "-"
            concerts_with_status.append({
                "concert": concert,
                "status": status,
            })

        return render(request, "concerts.html", {"concerts": concerts_with_status})

    return HttpResponseRedirect(reverse("login"))


def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Concert, pk=id)
        attendee = obj.attendee.filter(user=request.user).first()
        status = attendee.attending if attendee else "-"

        return render(request, "concert_detail.html", {
            "concert_details": obj,
            "status": status,
            "attending_choices": ConcertAttending.AttendingChoices.choices,
        })

    return HttpResponseRedirect(reverse("login"))


def concert_attendee(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method != "POST":
        return HttpResponseRedirect(reverse("concerts"))

    concert_id = request.POST.get("concert_id")
    attendee_status = request.POST.get("attendee_choice")

    if not concert_id or not attendee_status:
        return HttpResponseRedirect(reverse("concerts"))

    concert = get_object_or_404(Concert, pk=concert_id)

    concert_attendee_object = ConcertAttending.objects.filter(
        concert=concert,
        user=request.user,
    ).first()

    if concert_attendee_object:
        concert_attendee_object.attending = attendee_status
        concert_attendee_object.save()
    else:
        ConcertAttending.objects.create(
            concert=concert,
            user=request.user,
            attending=attendee_status,
        )

    return HttpResponseRedirect(reverse("concerts"))
