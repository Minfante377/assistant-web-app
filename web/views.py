from django.shortcuts import redirect, render
from django.urls import reverse


def index(request):
    """
    This view redirects the user to the login page.
    """
    return redirect(reverse('login'))


def login(request):
    """
    This view defines the login page.
    """
    return render(request, 'login.html')
