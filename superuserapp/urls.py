# DjangoVPS/superuserapp/urls.py

from django.urls import path
from . import views

app_name = 'superuserapp'

urlpatterns = [
    path('login/', views.SuperUserLoginView.as_view(), name='login'),
    path('panel/', views.PanelView.as_view(), name='panel'),
]