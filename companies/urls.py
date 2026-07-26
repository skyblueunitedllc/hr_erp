from django.urls import path
from .views import select_company

urlpatterns = [
    path('select-company/', select_company, name='select_company'),
]
