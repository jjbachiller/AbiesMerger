from django.shortcuts import render

def home_page():
    return render(request, 'home.html')
