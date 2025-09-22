# core/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from srcnn_project.supabase_client import supabase  

# supabase = settings.supabase

def home(request):
    return render(request, "home.html")

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        supabase.auth.sign_up({"email": email, "password": password})
        return redirect("login")
    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user:
            request.session["user"] = user.user.id
            return redirect("home")
    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")
