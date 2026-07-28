from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('create/', views.document_create, name='document_create'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('<int:pk>/renew/', views.document_renew, name='document_renew'),
    path('<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('<int:pk>/print/', views.document_print, name='document_print'),
    path('<int:pk>/download/', views.document_download, name='document_download'),
    path('<int:pk>/view/', views.document_view, name='document_view'),
]
