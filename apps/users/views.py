from django.shortcuts import render

def profile(request):
    return render(request, 'profile.html')

def auth(request):
    return render(request, 'auth.html')