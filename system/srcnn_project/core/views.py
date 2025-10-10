# core/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from srcnn_project.supabase_client import supabase  
import os
## can be a package
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
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

from django.shortcuts import render
from .forms import ImageUploadForm
from .ml.predictor import predict_pneumonia
import os
from django.conf import settings

def predict_view(request):
    result = None
    confidence = None

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]

            # Save temporarily
            img_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(img_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            # Predict
            result, confidence = predict_pneumonia(img_path)
            print(result, confidence)

    else:
        form = ImageUploadForm()

    return render(request, "upload.html", {"form": form, "result": result, "confidence": confidence})
