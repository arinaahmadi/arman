from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def start_view(request):
    return render(request,'managebar/index.html')
    