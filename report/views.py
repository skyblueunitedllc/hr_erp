from datetime import date
from django.shortcuts import render
from attendance.models import Attendance
from employees.models import Employee
from documents.models import Document


def dashboard(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name', '')

    heading_color = '#7e22ce'  # default purple

    if company_name:
        company_lower = company_name.lower()
        if 'skyblue united' in company_lower or 'skyblue' in company_lower:
            heading_color = '#2563eb'  # blue
        elif 'fana united' in company_lower or 'fana' in company_lower:
            heading_color = '#f97316'  # orange
        else:
            heading_color = '#7e22ce'  # purple

    total_employees = 0
    total_documents = 0
    total_attendances = 0
    total_payrolls = 0

    employee_expiring_documents = []
    company_expiring_documents = []
    present_attendance = Attendance.objects.none()

    if company_id:
        total_employees = Employee.objects.filter(company_id=company_id).count()
        total_documents = Document.objects.filter(company_id=company_id).count()

        present_attendance = Attendance.objects.filter(
            company_id=company_id,
            status__in=['present', 'half_day']
        ).select_related('employee').order_by('-date')
        total_attendances = present_attendance.count()

        # Employee documents expiring
        employee_docs = Document.objects.filter(
            company_id=company_id,
            is_company_document=False
        ).select_related('employee').order_by('expiry_date')

        # Company documents expiring
        company_docs = Document.objects.filter(
            company_id=company_id,
            is_company_document=True
        ).select_related('employee').order_by('expiry_date')

        today = date.today()

        def build_expiry_list(docs):
            items = []
            for doc in docs:
                if doc.expiry_date:
                    days_left = (doc.expiry_date - today).days
                    if days_left <= 30:
                        if days_left < 0:
                            alert_type = 'expired'
                            alert_label = 'Expired'
                        elif days_left <= 7:
                            alert_type = 'red'
                            alert_label = f'Critical ({days_left} days)'
                        elif days_left <= 15:
                            alert_type = 'orange'
                            alert_label = f'Expiring Soon ({days_left} days)'
                        else:
                            alert_type = 'yellow'
                            alert_label = f'Expiring ({days_left} days)'
                        items.append({
                            'title': doc.title,
                            'employee': doc.employee,
                            'expiry_date': doc.expiry_date,
                            'days_left': days_left,
                            'alert_type': alert_type,
                            'alert_label': alert_label,
                        })
            return items

        employee_expiring_documents = build_expiry_list(employee_docs)
        company_expiring_documents = build_expiry_list(company_docs)

        # Keep payroll count only if you have payroll model later
        total_payrolls = 0

    return render(request, 'reports/dashboard.html', {
        'company_name': company_name,
        'heading_color': heading_color,
        'total_employees': total_employees,
        'total_documents': total_documents,
        'employee_expiring_documents': employee_expiring_documents,
        'company_expiring_documents': company_expiring_documents,
        'total_attendances': total_attendances,
        'total_payrolls': total_payrolls,
        'present_attendance': present_attendance,
    })
