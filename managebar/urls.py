from django.urls import path
from managebar.views import start_view

urlpatterns = [
    path('',start_view)
]