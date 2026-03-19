from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")


def logout_view(request):

    logout(request)
    return redirect("login")
def signup_view(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request,"Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        return redirect("login")

    return render(request,"signup.html")