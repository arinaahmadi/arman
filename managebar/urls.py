from django.urls import path
from managebar.views import *

app_name = 'managebar'

urlpatterns = [
    path('',start_view,name='index'),
    path('about/',about_view,name='about'),
    path('home/',home_view,name='home'),
    path('practices/',practices_view,name='practices'),
    path('ourlawyers/',ourlawyers_view,name='ourlawyers'),
    path('bardetail/<str:shbar>',detail_view,name='bardetail'),
    path('barnameh/',barnameh_view,name='barnameh'),
    path('insertbank/',insertbank_view,name='insertbank'),
    path('banks/',banks_view,name='banks'),
    path('newbank/',createbank_view,name='newbank'),
    path('editbank/<int:bank_id>',editbank_view,name='editbank'),
    path('createdocx/',generate_contract,name='createdocx'),
    path('createxl/',excel_view,name='createxl'),
]