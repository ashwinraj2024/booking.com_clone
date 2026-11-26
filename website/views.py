from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import Http404
from django.shortcuts import redirect, render

# Sample data (no database needed for the pages)
HOTELS = [
    {"id": 1, "name": "The Palm Residency", "place": "Goa", "price": "₹4,200", "rating": "9.1",
     "emoji": "🏨", "description": "A relaxed stay with a pool, bright rooms and easy access to the beach."},
    {"id": 2, "name": "Lakeview Retreat", "place": "Udaipur", "price": "₹5,600", "rating": "8.8",
     "emoji": "🏰", "description": "A peaceful hotel with lake views and a warm, welcoming atmosphere."},
    {"id": 3, "name": "Mountain Nest", "place": "Manali", "price": "₹3,500", "rating": "8.9",
     "emoji": "🏔️", "description": "A cosy mountain escape surrounded by beautiful natural scenery."},
    {"id": 4, "name": "The Capital Suites", "place": "New Delhi", "price": "₹6,800", "rating": "8.7",
     "emoji": "🏢", "description": "Modern suites close to the metro, markets and major sightseeing spots."},
    {"id": 5, "name": "Garden City Inn", "place": "Bangalore", "price": "₹4,900", "rating": "8.5",
     "emoji": "🌳", "description": "A comfortable hotel with a rooftop cafe and fast Wi-Fi."},
    {"id": 6, "name": "Pink City Haveli", "place": "Jaipur", "price": "₹5,100", "rating": "9.0",
     "emoji": "🕌", "description": "A heritage haveli with courtyard dining and traditional rooms."},
]


def home(request):
    return render(request, "website/home.html", {"featured": HOTELS[:3]})


def stays(request):
    destination = request.GET.get("destination", "").strip()
    hotels = HOTELS
    if destination:
        hotels = [h for h in HOTELS if destination.lower() in h["place"].lower()]
    return render(request, "website/stays.html", {"hotels": hotels, "destination": destination})


def hotel_detail(request, hotel_id):
    for hotel in HOTELS:
        if hotel["id"] == hotel_id:
            return render(request, "website/hotel_detail.html", {"hotel": hotel})
    raise Http404("Property not found")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        if not email or not password:
            messages.error(request, "Please enter your email and password.")
        else:
            user = authenticate(request, username=email, password=password)
            if user is None:
                messages.error(request, "Email or password is incorrect.")
            else:
                login(request, user)
                messages.success(request, "Welcome back, " + user.first_name + "!")
                return redirect("home")
    return render(request, "website/login.html")


def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")

        try:
            validate_email(email)
            email_ok = True
        except ValidationError:
            email_ok = False

        if not name or not email or not password or not confirm:
            messages.error(request, "Please fill in every field.")
        elif not email_ok:
            messages.error(request, "Please enter a valid email address.")
        elif len(password) < 8:
            messages.error(request, "Your password must be at least 8 characters long.")
        elif password != confirm:
            messages.error(request, "The passwords do not match.")
        elif User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
        else:
            # create_user stores the password as a hash, never as plain text
            User.objects.create_user(username=email, email=email, password=password, first_name=name)
            messages.success(request, "Your account has been created. Please log in.")
            return redirect("login")
    return render(request, "website/signup.html")
