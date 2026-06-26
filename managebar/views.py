from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from managebar.models import Barnameh
from django.contrib.auth.decorators import login_required

@login_required
def start_view(request):
    barnameha = Barnameh.objects.all()
    context = {'barnames':barnameha}
    return render(request,'managebar/index.html',context)

def barnameh_view(request):
    barnameha = Barnameh.objects.all()
    context = {'barnames':barnameha}
    return render(request,'managebar/barnameh.html',context)

def insertbank_view(request):
    if request.method == 'POST':
        print('Done')
    return render(request,'managebar/insertbank.html')

def about_view(request):
    return render(request,'managebar/about.html')

def home_view(request):
    return render(request,'managebar/home.html')

def practices_view(request):
    barnameha = Barnameh.objects.all()
    context = {'barnames':barnameha}
    # print(type(barnameha))
    return render(request,'managebar/practices.html',context)

def detail_view(request,shbar):
    # shbarname = shbar

    try:
        barnameh = Barnameh.objects.get(shbarnameh=shbar)
    except Barnameh.DoesNotExist:
        barnameh = None

    context = {'barnameh':barnameh}
    # context = {'shbar':shbar}
    return render(request,'managebar/detailbar.html',context)
    

    
def ourlawyers_view(request):
    return render(request,'managebar/ourlawyers.html')    
    