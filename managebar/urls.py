from django.urls import path
from managebar.views import *


urlpatterns = [
    path('',start_view),
    path('page2/',page2_view),
    path('page3/',page3_view),
]