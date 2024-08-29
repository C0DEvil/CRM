from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("home")

    return render(request, "home.html", {"records": records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!.")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered successfully!.")
            return redirect("home")
        else:
            messages.error(request, form.errors)
            return redirect("register")
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})


def costumer_record(request, pk):
    if request.user.is_authenticated:
        # look up for records
        costumer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"costumer_record": costumer_record})
    else:
        messages.error(request, "You must be logged in to view the page")
        return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        # look up for records
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted")
        return redirect("home")

    else:
        messages.error(request, "You must be logged in to view the page")
        return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added")
                return redirect("home")
            else:
                messages.error(request, form.errors)
                return redirect("add_record")
        return render(request, "add_record.html", {"form": form})
    else:
        messages.error(request, "You must be logged in to view the page")
        return redirect("home")

def update_record(request,pk):
     if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if request.method == "POST":
           if form.is_valid():
               form.save()
               messages.success(request, "Record updated")
               return redirect("home")
        else:
           return  render(request,'update_record.html',{'form': form})
     
     else:
        messages.error(request, "You must be logged in to view the page")
        return redirect("home")