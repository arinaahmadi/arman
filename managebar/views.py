from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def start_view(request):
    return render(request,'managebar/index.html')

def page2_view(request):
    return render(request,'managebar/page2.html')

def page3_view(request):
    return render(request,'managebar/page3.html')
    
    