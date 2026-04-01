from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse


from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending


# Create your views here.

# Define the signup view that handles user registration requests.
def signup(request):
    # Check whether the incoming request submitted the signup form with POST.
    if request.method == "POST":
        # Read the username value from the submitted form data.
        user_name = request.POST.get("username")
        # Read the password value from the submitted form data.
        user_pwd = request.POST.get("password")

        # Stop and re-render the form if either field was left empty.
        if not user_name or not user_pwd:
            # Render the signup page again and send a validation message back to the template.
            return render(request, "signup.html", {
                # Create a fresh signup form instance for the template.
                "form": SignUpForm(),
                # Provide the validation error message to display to the user.
                "message": "Username and password are required",
            })

        # Look up the first user whose username matches the submitted username.
        user = User.objects.filter(username=user_name).first()
        # If a matching user already exists, prevent duplicate account creation.
        if user:
            # Render the signup page again and explain that the username is already taken.
            return render(request, "signup.html", {
                # Create a fresh signup form instance for the template.
                "form": SignUpForm(),
                # Provide the duplicate-username message to display to the user.
                "message": "Username already exists",
            })

        # Create a new Django user using the submitted username and password.
        # `User.objects.create(...)` can also create a row, but `create_user(...)`
        # is the correct auth helper because it hashes the password properly and
        # applies Django's standard user-creation behavior automatically.
        user = User.objects.create_user(username=user_name, password=user_pwd)
        # Log the new user in immediately after successful account creation.
        login(request, user)
        # Redirect the browser to the index page after signup succeeds.
        return HttpResponseRedirect(reverse("index"))

    # Render the signup page for non-POST requests such as the initial page load.
    return render(request, "signup.html", {"form": SignUpForm()})


# Define the index view for the application's home page.
def index(request):
    # Render and return the home page template.
    return render(request, "index.html")



# Define a view function named 'songs' that takes an HTTP request object as its parameter
def songs(request):
    # Create a dictionary with a single key "songs" that contains a list of song dictionaries
    songs = {"songs":[
        # Start a dictionary representing one song record.
        {
            # Store the unique identifier for this song entry.
            "id":1,
            # Store the title text for this song entry.
            "title":"duis faucibus accumsan odio curabitur convallis",
            # The lyrics field uses parentheses for implicit string concatenation across multiple lines
            # (no + operator needed)
            # Store the lyrics text for this song entry.
            "lyrics":("Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. " 
                      "Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis."
                      )
        }
    ]}
    # Call render() with: the request object, template path, and context dictionary
    # - note that songs["songs"] extracts the list from the outer dictionary before passing it to the template
    return render(request, "songs.html", {"songs": songs["songs"]})

# Define the photos view that supplies photo data to the template.
def photos(request):
    # Create a list containing one photo dictionary to pass to the page.
    photos = [{
    # Store the unique identifier for this photo entry.
    "id": 1,
    # Store the image URL for this photo entry.
    "pic_url": "http://dummyimage.com/136x100.png/5fa2dd/ffffff",
    # Store the country where the event took place.
    "event_country": "United States",
    # Store the state where the event took place.
    "event_state": "District of Columbia",
    # Store the city where the event took place.
    "event_city": "Washington",
    # Store the event date for this photo entry.
    "event_date": "11/16/2022"
}]

    # Render the photos page and pass the photo list into the template context.
    return render(request, "photos.html", {"photos": photos})

# Define the login view that handles authentication requests.
def login_view(request):
    # Check whether the login form was submitted with POST.
    if request.method == "POST":
        # Read the submitted username from the form data.
        username = request.POST.get("username")
        # Read the submitted password from the form data.
        password = request.POST.get("password")
        # Look up the first user whose username matches the submitted username.
        user = User.objects.filter(username=username).first()
        # If a user was found and the password matches, log the user in.
        if user and user.check_password(password):
            # Create an authenticated session for the matching user.
            login(request, user)
            # Redirect the browser to the index page after a successful login.
            return HttpResponseRedirect(reverse("index"))

        # Re-render the login page with an invalid-credentials message when authentication fails.
        return render(request, "login.html", {"form": LoginForm(), "message": "Invalid Credentials"})

    # Render the login page for non-POST requests such as the first visit.
    return render(request, "login.html", {"form": LoginForm()})

# Define the logout view that ends the user's authenticated session.
def logout_view(request):
    # Log the current user out of the session.
    logout(request)
    # Redirect the browser to the login page after logout.
    return HttpResponseRedirect(reverse("login"))


# Define the concerts view that lists concerts and the current user's attendance status.
def concerts(request):
    # Get the currently logged-in user from the request object.
    user = request.user
    # Only allow authenticated users to access the concerts page.
    if user.is_authenticated:
        # Create an empty list that will store each concert plus its attendance status.
        concerts_with_status = []
        # Query the database for all concert records.
        concert_objects = Concert.objects.all()

        # Loop through each concert so status can be calculated per concert.
        for concert in concert_objects:
            # Look up the current user's attendance record for this concert, if one exists.
            attendee = concert.attendee.filter(user=user).first()
            # Use the saved attendance choice when present, otherwise use a dash placeholder.
            status = attendee.attending if attendee else "-"
            # Add the concert object and computed status to the list sent to the template.
            concerts_with_status.append({
                # Store the current concert object under the key expected by the template.
                "concert": concert,
                # Store the attendance status for the current concert.
                "status": status,
            })

        # Render the concerts page and provide the prepared concert list to the template.
        return render(request, "concerts.html", {"concerts": concerts_with_status})

    # Redirect unauthenticated users to the login page.
    return HttpResponseRedirect(reverse("login"))


# Define the concert-detail view for one specific concert.
def concert_detail(request, id):
    # Only allow authenticated users to access a concert's detail page.
    if request.user.is_authenticated:
        # Fetch the concert by primary key or return a 404 page if it does not exist.
        obj = get_object_or_404(Concert, pk=id)
        # Look up the current user's attendance record for this concert, if one exists.
        attendee = obj.attendee.filter(user=request.user).first()
        # Use the saved attendance value when found, otherwise fall back to a dash placeholder.
        status = attendee.attending if attendee else "-"

        # Render the concert detail page and pass the concert data, status, and choices to the template.
        return render(request, "concert_detail.html", {
            # Pass the selected concert object into the template context.
            "concert_details": obj,
            # Pass the current user's attendance status into the template context.
            "status": status,
            # Pass the available attendance choices defined on the model into the template context.
            "attending_choices": ConcertAttending.AttendingChoices.choices,
        })

    # Redirect unauthenticated users to the login page.
    return HttpResponseRedirect(reverse("login"))


# Define the view that creates or updates a user's concert attendance choice.
def concert_attendee(request):
    # Redirect to the index page if the user is not logged in.
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # Reject non-POST requests because this view is intended to process form submissions only.
    if request.method != "POST":
        return HttpResponseRedirect(reverse("concerts"))

    # Read the concert identifier from the submitted form data.
    concert_id = request.POST.get("concert_id")
    # Read the chosen attendance status from the submitted form data.
    attendee_status = request.POST.get("attendee_choice")

    # Redirect back to the concerts page if either required form value is missing.
    if not concert_id or not attendee_status:
        return HttpResponseRedirect(reverse("concerts"))

    # Fetch the referenced concert or return a 404 page if the ID is invalid.
    concert = get_object_or_404(Concert, pk=concert_id)

    # Look for an existing attendance record for this user and concert pair.
    concert_attendee_object = ConcertAttending.objects.filter(
        # Match records for the selected concert.
        concert=concert,
        # Match records for the current logged-in user.
        user=request.user,
    ).first()

    # If an attendance record already exists, update its status.
    if concert_attendee_object:
        # Replace the old attendance value with the newly submitted choice.
        concert_attendee_object.attending = attendee_status
        # Save the updated attendance record to the database.
        concert_attendee_object.save()
    else:
        # Otherwise create a brand-new attendance record for this user and concert.
        ConcertAttending.objects.create(
            # Store the selected concert on the new attendance record.
            concert=concert,
            # Store the current logged-in user on the new attendance record.
            user=request.user,
            # Store the submitted attendance choice on the new attendance record.
            attending=attendee_status,
        )

    # Redirect the browser back to the concerts page after processing the form.
    return HttpResponseRedirect(reverse("concerts"))
