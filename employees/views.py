from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Employee
from .forms import EmployeeForm


def employee_list(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')
    query = request.GET.get('q', '')

    employees = Employee.objects.none()

    if company_id:
        employees = Employee.objects.filter(company_id=company_id)

        if query:
            employees = employees.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        employees = employees.order_by('first_name', 'last_name')

    return render(request, 'employees/employee_list.html', {
        'employees': employees,
        'company_name': company_name,
        'query': query,
    })


def employee_create(request):
    company_id = request.session.get('company_id')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if company_id:
            form.fields['company'].initial = company_id
            form.fields['company'].widget.attrs['readonly'] = True
        if form.is_valid():
            employee = form.save(commit=False)
            if company_id:
                employee.company_id = company_id
            employee.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
        if company_id:
            form.fields['company'].initial = company_id
            form.fields['company'].widget.attrs['readonly'] = True

    if company_id:
        form.fields['company'].queryset = form.fields['company'].queryset.filter(id=company_id)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add Employee',
    })


def employee_update(request, pk):
    company_id = request.session.get('company_id')
    employee = get_object_or_404(Employee, pk=pk, company_id=company_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if company_id:
            form.fields['company'].initial = company_id
            form.fields['company'].widget.attrs['readonly'] = True
        if form.is_valid():
            emp = form.save(commit=False)
            if company_id:
                emp.company_id = company_id
            emp.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
        if company_id:
            form.fields['company'].initial = company_id
            form.fields['company'].widget.attrs['readonly'] = True

    if company_id:
        form.fields['company'].queryset = form.fields['company'].queryset.filter(id=company_id)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Edit Employee',
    })


def employee_delete(request, pk):
    company_id = request.session.get('company_id')
    employee = get_object_or_404(Employee, pk=pk, company_id=company_id)

    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')

    return render(request, 'employees/employee_confirm_delete.html', {
        'employee': employee
    })
