from django.urls import path
from . import views

urlpatterns = [
    path("", views.payroll_list, name="payroll_list"),
    path("add/", views.payroll_create, name="payroll_create"),
    path("<int:pk>/edit/", views.payroll_update, name="payroll_update"),
    path("<int:pk>/delete/", views.payroll_delete, name="payroll_delete"),
    path("<int:pk>/print/", views.payroll_print, name="payroll_print"),
]
