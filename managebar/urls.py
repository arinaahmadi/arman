from django.urls import path
from managebar.views import *

app_name = 'managebar'

urlpatterns = [
    path('',start_view,name='index'),
    path('projs/',page2_view,name='projs'),
    path('page3/',page3_view),
]