from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from managebar.models import Barnameh, Bank
from django.contrib.auth.decorators import login_required
from managebar.forms import BankForm


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

def banks_view(request):
    banks = Bank.objects.all()
    context = {'banks':banks}
    return render(request,'managebar/banks.html',context) 
    

def createbank_view(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            # print("cleaned_data =", form.cleaned_data)
            form.save()
            return redirect('managebar:banks')  # نام url صفحه‌ای که لیست گروه‌ها/کاربرها را نشان می‌دهد
        else:
            print("start")
            print(form.errors)   # برای دیباگ
            print("end")
    else:
        form = BankForm()

    return render(request, 'managebar/createbank.html', {'form': form})


def editbank_view(request,bank_id):
    bank = get_object_or_404(Bank, id=bank_id)

    if request.method == 'POST':
        form = BankForm(request.POST, instance=bank)
        if form.is_valid():
            # print("cleaned_data =", form.cleaned_data)
            form.save()
            return redirect('managebar:banks')  # نام url صفحه‌ای که لیست گروه‌ها/کاربرها را نشان می‌دهد
        else:
            print("start")
            print(form.errors)   # برای دیباگ
            print("end")
    else:
        form = BankForm(instance=bank)

    return render(request, 'managebar/editbank.html', {'bank_id':bank_id,'form': form})
