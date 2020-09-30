from django.urls import path
from .views import items_list

app_name = 'core'

urlpatterns = [
    path('', items_list, name = 'items_list')
]