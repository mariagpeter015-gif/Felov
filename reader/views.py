from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Book

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['name'], password=request.POST['pwd'])
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'log.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('mail')
        username = request.POST.get('uname')
        password = request.POST.get('pwd')

        user = User.objects.create_user(username=username, password=password, email=email, first_name=full_name)
        login(request, user)
        return redirect('home')

    return render(request, 'reg.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'home.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')

        Book.objects.create(title=title, author=author, description=description, user=request.user)

        return redirect('home')
    return render(request, 'add.html')

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.description = request.POST['description']
        book.is_finished = 'is_finished' in request.POST
        book.save()
        return redirect('home')
    return render(request, 'edit.html', {'book': book})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('home')
    return redirect('book_detail', book_id=book_id)

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    return render(request, 'book_detail.html', {'book': book})

