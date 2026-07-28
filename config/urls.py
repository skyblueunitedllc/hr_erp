from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from accounts.views import login_view
from django.contrib.auth import views as auth_views
from companies import views as company_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', lambda request: redirect('/login/')),
    path('select-company/', company_views.select_company, name='select_company'),
    path('companies/', include('companies.urls')),
    path('employees/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
    path('documents/', include('documents.urls')),
    path('payroll/', include('payroll.urls')),
    path('report/', include('report.urls')),
]
