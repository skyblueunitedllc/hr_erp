from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from employees.models import Employee
from .models import Attendance, Overtime
from .forms import AttendanceForm, OvertimeForm


def attendance_list(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')
    query = request.GET.get('q', '')

    attendance_records = Attendance.objects.none()

    if company_id:
        attendance_records = Attendance.objects.filter(company_id=company_id).select_related('employee', 'company')

        if query:
            attendance_records = attendance_records.filter(
                Q(employee__first_name__icontains=query) |
                Q(employee__last_name__icontains=query)
            )

        attendance_records = attendance_records.order_by('-date')

    return render(request, 'attendance/attendance_list.html', {
        'attendance_records': attendance_records,
        'company_name': company_name,
        'query': query,
    })


def attendance_create(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('select_company')

    employees = Employee.objects.filter(company_id=company_id).order_by('first_name', 'last_name')

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        form.fields['employee'].queryset = employees
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.company_id = company_id
            attendance.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
        form.fields['employee'].queryset = employees

    return render(request, 'attendance/attendance_form.html', {
        'form': form,
        'title': 'Add Attendance',
        'company_name': request.session.get('company_name'),
    })


def attendance_update(request, pk):
    company_id = request.session.get('company_id')
    attendance = get_object_or_404(Attendance, pk=pk, company_id=company_id)
    employees = Employee.objects.filter(company_id=company_id).order_by('first_name', 'last_name')

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        form.fields['employee'].queryset = employees
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.company_id = company_id
            attendance.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
        form.fields['employee'].queryset = employees

    return render(request, 'attendance/attendance_form.html', {
        'form': form,
        'title': 'Edit Attendance',
        'company_name': request.session.get('company_name'),
    })


def attendance_delete(request, pk):
    company_id = request.session.get('company_id')
    attendance = get_object_or_404(Attendance, pk=pk, company_id=company_id)

    if request.method == 'POST':
        attendance.delete()
        return redirect('attendance_list')

    return render(request, 'attendance/attendance_confirm_delete.html', {
        'attendance': attendance,
    })


def overtime_list(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')
    query = request.GET.get('q', '')

    overtimes = Overtime.objects.none()

    if company_id:
        overtimes = Overtime.objects.filter(company_id=company_id).select_related('employee', 'company')

        if query:
            overtimes = overtimes.filter(
                Q(employee__first_name__icontains=query) |
                Q(employee__last_name__icontains=query)
            )

        overtimes = overtimes.order_by('-work_date', '-id')

    total_by_employee = overtimes.values(
        'employee__first_name', 'employee__last_name'
    ).annotate(
        total_hours=Sum('hours'),
        total_amount=Sum('amount')
    )

    return render(request, 'attendance/overtime_list.html', {
        'overtimes': overtimes,
        'company_name': company_name,
        'query': query,
        'total_by_employee': total_by_employee,
    })


def overtime_create(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('select_company')

    employees = Employee.objects.filter(company_id=company_id).order_by('first_name', 'last_name')

    if request.method == 'POST':
        form = OvertimeForm(request.POST)
        form.fields['employee'].queryset = employees
        if form.is_valid():
            overtime = form.save(commit=False)
            overtime.company_id = company_id
            overtime.save()
            return redirect('overtime_list')
    else:
        form = OvertimeForm()
        form.fields['employee'].queryset = employees

    return render(request, 'attendance/overtime_form.html', {
        'form': form,
        'title': 'Add Overtime',
        'company_name': request.session.get('company_name'),
    })


def overtime_update(request, pk):
    company_id = request.session.get('company_id')
    overtime = get_object_or_404(Overtime, pk=pk, company_id=company_id)
    employees = Employee.objects.filter(company_id=company_id).order_by('first_name', 'last_name')

    if request.method == 'POST':
        form = OvertimeForm(request.POST, instance=overtime)
        form.fields['employee'].queryset = employees
        if form.is_valid():
            overtime = form.save(commit=False)
            overtime.company_id = company_id
            overtime.save()
            return redirect('overtime_list')
    else:
        form = OvertimeForm(instance=overtime)
        form.fields['employee'].queryset = employees

    return render(request, 'attendance/overtime_form.html', {
        'form': form,
        'title': 'Edit Overtime',
        'company_name': request.session.get('company_name'),
    })


def overtime_delete(request, pk):
    company_id = request.session.get('company_id')
    overtime = get_object_or_404(Overtime, pk=pk, company_id=company_id)

    if request.method == 'POST':
        overtime.delete()
        return redirect('overtime_list')

    return render(request, 'attendance/overtime_confirm_delete.html', {
        'overtime': overtime,
    })
