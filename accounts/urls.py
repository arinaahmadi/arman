from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('users',users_view,name='users'),
    path('newgroup/',new_group_view,name='newgroup'),
    path('groups/<int:group_id>/edit/', edit_group_view, name='edit_group'),
]