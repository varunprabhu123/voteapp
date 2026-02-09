from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import VotePoll, VoterRecord
from .forms import VotingForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def Register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(email=email).exists():
            messages.error(request, "The email is already registered")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Successfully registered! Please log in.")
            return redirect("login")

    return render(request, "register.html")

def Login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect("vote")
        messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})

def Logout_view(request):
    logout(request)
    # messages.info(request, "You have logged out successfully.")
    return redirect("login")

@login_required(login_url='login')
def Vote_view(request):
    voter, created = VoterRecord.objects.get_or_create(user_name=request.user)

    if voter.has_voted:
        messages.warning(request, "You have already cast your vote!")
        return redirect("results")

    if request.method == "POST":
        form = VotingForm(request.POST)
        if form.is_valid():
            candidate = form.cleaned_data["candidate"]
            candidate.vote += 1
            candidate.save()

            voter.has_voted = True
            voter.save()
            return redirect("results")
    else:
        form = VotingForm()

    return render(request, "vote.html", {"form": form})

# @login_required(login_url='login')
def view_result(request):
    candidates = VotePoll.objects.all().order_by("-vote")
    color=["bg-success","bg-info","bg-warning","bg-danger","bg-primary"]
    candidates_with_color = [
        (candidate, color[i % len(color)]) for i, candidate in enumerate(candidates)
    ]
    return render(request, "results.html", {"candidates_with_color":candidates_with_color})
