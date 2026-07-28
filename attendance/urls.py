from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('add/', views.attendance_create, name='attendance_create'),
    path('<int:pk>/edit/', views.attendance_update, name='attendance_update'),
    path('<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),

    path('overtime/', views.overtime_list, name='overtime_list'),
    path('overtime/add/', views.overtime_create, name='overtime_create'),
    path('overtime/<int:pk>/', views.overtime_detail, name='overtime_detail'),
    path('overtime/<int:pk>/edit/', views.overtime_update, name='overtime_update'),
    path('overtime/<int:pk>/delete/', views.overtime_delete, name='overtime_delete'),
    path('overtime/print/', views.overtime_print, name='overtime_print'),
]
