from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if 'email' in request.session.keys():
        return redirect ('login/success')
    return render(request, "logandreg/index.html")

def reg(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/login')
    else:
        userpass = request.POST['pw']
        hashpass = bcrypt.hashpw(userpass.encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashpass)
        temp = User.objects.last()
        request.session['name'] = temp.first_name
        request.session['email'] = temp.email
        request.session['validation'] = "registered!"
    return redirect ('/login/success')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/login')
    else:
        temp = User.objects.filter(email = request.POST['logEmail'])
        print temp[0].first_name
        request.session['name'] = temp[0].first_name
        request.session['email'] = temp[0].email
        request.session['validation'] = "logged in!"
        return redirect("/login/success")

def success(request):
    return render(request, "logandreg/success.html")