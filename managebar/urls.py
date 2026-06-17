from django.urls import path
from managebar.views import *

app_name = 'managebar'

urlpatterns = [
    path('',start_view,name='index'),
    path('about/',about_view,name='about'),
    path('home/',home_view,name='home'),
    path('practices/',practices_view,name='practices'),
    path('ourlawyers/',ourlawyers_view,name='ourlawyers'),
    path('bardetail/<str:shbar>',detail_view,name='bardetail')

]