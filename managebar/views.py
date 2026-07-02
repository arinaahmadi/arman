from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
# Create your views here.
from django.http import HttpResponse
from managebar.models import Barnameh, Bank
from django.contrib.auth.decorators import login_required
from managebar.forms import BankForm
from django.conf import settings
from docxtpl import DocxTemplate
import os
from datetime import datetime
import pandas as pd



def excel_view(request):
    # پسوند فایل را هم مطمئن شوید که اکسل است (مثلاً xlsx)
    template_path = os.path.join(
        settings.BASE_DIR, "docx_templates", "excel1.xlsx"
    )

    # بررسی وجود فایل برای جلوگیری از خطای FileNotFoundError
    # if not os.path.exists(template_path):
    #     return HttpResponse(
    #         f"فایل در مسیر زیر پیدا نشد:<br>{template_path}", status=404
    #     )

    # try:
    df = pd.read_excel(template_path)

    row_count = len(df)
        # پردازش ردیف‌ها
    for index, row in df.iterrows():
        print(f"Index: {index}")
        print(f"Name: {row['نام راننده اول']}")
    
    # print(f"تعداد رکوردها: {row_count}")
    rows, columns = df.shape

    print("تعداد ردیف‌ها:", rows)
    print("تعداد ستون‌ها:", columns)

    data = [
        {'نام': 'علی', 'شماره بارنامه': '12345', 'مبلغ': 50000},
        {'نام': 'رضا', 'شماره بارنامه': '67890', 'مبلغ': 75000},
    ]

    df = pd.DataFrame(data)

    output_dir = os.path.join(settings.MEDIA_ROOT, "docxfile")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "output.xlsx")


    df.to_excel(output_path, index=False)

        # بازگرداندن پاسخ به مرورگر کاربر
    return HttpResponse(
        "فایل اکسل با موفقیت خوانده شد و داده‌ها در ترمینال چاپ شدند."
    )

    # except Exception as e:
    #     return HttpResponse(f"خطایی در پردازش فایل رخ داد: {str(e)}", status=500)


def generate_contract(request):
    template_path = os.path.join(settings.BASE_DIR, "docx_templates", "trafic.docx")

    output_dir = os.path.join(settings.MEDIA_ROOT, "docxfile")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "contract.docx")

    doc = DocxTemplate(template_path)

    context = {
        "company_name": "شرکت ملی صنایع مس ایران",
        "from_co": "رابر"
    }

    doc.render(context)
    doc.save(output_path)

    # return FileResponse(open(output_path, "rb"), as_attachment=True, filename="contract-1.docx")
    return HttpResponse("Contract created successfully.")




#     template_path = os.path.join(
#         settings.BASE_DIR,
#         "docx_templates",
#         "trafic.docx"
#     )
#     doc = DocxTemplate(template_path)
#     context = {
#         "company_name": "شرکت ملی صنایع مس ایران",
#         "from_co": "رابر"
#     }
#     doc.render(context)

# #   وقتی می خوای فایل ذخیره شود
#     output_dir = os.path.join(settings.MEDIA_ROOT, "contracts")
#     os.makedirs(output_dir, exist_ok=True)

#     output_path = os.path.join(output_dir, "contract-1.docx")
# #   وقتی می خوای فایل ذخیره شود

#     response = HttpResponse(
#         content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#     )
#     response["Content-Disposition"] = 'attachment; filename="contract.docx"'
#     doc.save(response)
#     return response


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
