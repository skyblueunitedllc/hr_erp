from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from .models import Attendance, Overtime
from .forms import AttendanceForm, OvertimeForm
from employees.models import Employee
from companies.models import Company


def _format_display_date(value):
    if not value:
        return ""
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").strftime("%d-%m-%Y")
    except Exception:
        return str(value)


@login_required
def attendance_list(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')
    query = request.GET.get('q', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    attendances = Attendance.objects.none()

    if company_id:
        attendances = Attendance.objects.filter(company_id=company_id).select_related('employee', 'company')

        if query:
            attendances = attendances.filter(
                Q(employee__first_name__icontains=query) |
                Q(employee__last_name__icontains=query)
            )

        if from_date:
            attendances = attendances.filter(date__gte=from_date)

        if to_date:
            attendances = attendances.filter(date__lte=to_date)

    attendances = attendances.order_by('-date', '-id')

    return render(request, 'attendance/attendance_list.html', {
        'attendances': attendances,
        'query': query,
        'from_date': from_date,
        'to_date': to_date,
        'company_name': company_name,
    })


@login_required
def attendance_create(request):
    company_id = request.session.get('company_id')

    if not company_id:
        messages.error(request, "Please select a company first.")
        return redirect('select_company')

    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.company = company
            attendance.save()
            messages.success(request, "Attendance created successfully.")
            return redirect('attendance_list')
    else:
        form = AttendanceForm()

    return render(request, 'attendance/attendance_form.html', {'form': form})


@login_required
def attendance_update(request, pk):
    company_id = request.session.get('company_id')
    attendance = get_object_or_404(Attendance, pk=pk, company_id=company_id)

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance updated successfully.")
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'attendance/attendance_form.html', {'form': form})


@login_required
def attendance_delete(request, pk):
    company_id = request.session.get('company_id')
    attendance = get_object_or_404(Attendance, pk=pk, company_id=company_id)

    if request.method == 'POST':
        attendance.delete()
        messages.success(request, "Attendance deleted successfully.")
        return redirect('attendance_list')

    return render(request, 'attendance/attendance_confirm_delete.html', {'attendance': attendance})


@login_required
def overtime_list(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')
    query = request.GET.get('q', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    status = request.GET.get('status', '')

    overtimes = Overtime.objects.none()

    if company_id:
        overtimes = Overtime.objects.filter(company_id=company_id).select_related('employee', 'company')

        if query:
            overtimes = overtimes.filter(
                Q(employee__first_name__icontains=query) |
                Q(employee__last_name__icontains=query)
            )

        if from_date:
            overtimes = overtimes.filter(work_date__gte=from_date)

        if to_date:
            overtimes = overtimes.filter(work_date__lte=to_date)

        if status == 'paid':
            overtimes = overtimes.filter(paid=True)
        elif status == 'unpaid':
            overtimes = overtimes.filter(paid=False)

    overtimes = overtimes.order_by('-work_date', '-id')

    return render(request, 'attendance/overtime_list.html', {
        'overtimes': overtimes,
        'query': query,
        'from_date': from_date,
        'to_date': to_date,
        'status': status,
        'company_name': company_name,
    })


@login_required
def overtime_create(request):
    company_id = request.session.get('company_id')

    if not company_id:
        messages.error(request, "Please select a company first.")
        return redirect('select_company')

    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        form = OvertimeForm(request.POST)
        if form.is_valid():
            overtime = form.save(commit=False)
            overtime.company = company
            overtime.save()
            messages.success(request, "Overtime created successfully.")
            return redirect('overtime_list')
    else:
        form = OvertimeForm()

    return render(request, 'attendance/overtime_form.html', {'form': form})


@login_required
def overtime_update(request, pk):
    company_id = request.session.get('company_id')
    overtime = get_object_or_404(Overtime, pk=pk, company_id=company_id)

    if request.method == 'POST':
        form = OvertimeForm(request.POST, instance=overtime)
        if form.is_valid():
            form.save()
            messages.success(request, "Overtime updated successfully.")
            return redirect('overtime_list')
    else:
        form = OvertimeForm(instance=overtime)

    return render(request, 'attendance/overtime_form.html', {'form': form})


@login_required
def overtime_delete(request, pk):
    company_id = request.session.get('company_id')
    overtime = get_object_or_404(Overtime, pk=pk, company_id=company_id)

    if request.method == 'POST':
        overtime.delete()
        messages.success(request, "Overtime deleted successfully.")
        return redirect('overtime_list')

    return render(request, 'attendance/overtime_confirm_delete.html', {'overtime': overtime})


@login_required
def overtime_detail(request, pk):
    company_id = request.session.get('company_id')
    overtime = get_object_or_404(Overtime, pk=pk, company_id=company_id)

    return render(request, 'attendance/overtime_detail.html', {
        'overtime': overtime,
    })
@login_required
def overtime_print(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')
    query = request.GET.get('q', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    status = request.GET.get('status', '')

    overtimes = Overtime.objects.none()

    if company_id:
        overtimes = Overtime.objects.filter(company_id=company_id).select_related('employee', 'company')

        if query:
            overtimes = overtimes.filter(
                Q(employee__first_name__icontains=query) |
                Q(employee__last_name__icontains=query)
            )

        if from_date:
            overtimes = overtimes.filter(work_date__gte=from_date)

        if to_date:
            overtimes = overtimes.filter(work_date__lte=to_date)

        if status == 'paid':
            overtimes = overtimes.filter(paid=True)
        elif status == 'unpaid':
            overtimes = overtimes.filter(paid=False)

        overtimes = overtimes.order_by('work_date', 'id')

        for overtime in overtimes:
            overtime.paid = True
            if not overtime.paid_date:
                overtime.paid_date = datetime.now().date()
            overtime.save()

    total_hours = sum(float(o.hours) for o in overtimes)
    total_amount = sum(float(o.amount) for o in overtimes)

    employee_name = ""
    if overtimes.exists():
        first = overtimes.first()
        employee_name = f"{first.employee.first_name} {first.employee.last_name}"

    return render(request, 'attendance/overtime_print.html', {
        'overtimes': overtimes,
        'employee_name': employee_name,
        'company_name': company_name,
        'from_date_display': _format_display_date(from_date),
        'to_date_display': _format_display_date(to_date),
        'total_hours': total_hours,
        'total_amount': total_amount,
    })
