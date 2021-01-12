from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    return render(request, "index.html")

## Login and Register

def register(request):
    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        else:
            password = request.POST['pword']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            new_user = User.objects.create(
                name=request.POST['name'],
                username=request.POST['username'],
                email=request.POST['email'],
                pword=pw_hash
            )
            request.session['user_id']=new_user.id
            return redirect('/books')
    return redirect('/')

def login(request):
    if request.method=='POST':
        errors=User.objects.login_validator(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        logged_user = User.objects.filter(email=request.POST['login_email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['login_pword'].encode(), logged_user.pword.encode()):
                request.session['user_id']=logged_user.id
                return redirect('/books')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

## Book Dashboard

def books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context={
        "all_books": Book.objects.all(),
        "all_reviews": Review.objects.all(),
        "current_user": User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'home.html', context)

def add_book(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context={
        "current_user": User.objects.get(id=request.session['user_id']),
        "all_authors": Author.objects.all(),
    }
    return render(request, 'add_book.html', context)

def create_book(request):
    errors=Book.objects.book_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/books/add')
    