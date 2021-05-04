from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")

def book(request):
    return render(request, "book_details.html")