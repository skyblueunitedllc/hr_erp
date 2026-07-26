from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from companies.models import Company
from .models import Payroll
from .forms import PayrollForm


@login_required
def payroll_list(request):
    company_id = request.session.get("company_id")
    company_name = request.session.get("company_name")

    employee_name = request.GET.get("employee_name", "").strip()
    employee_code = request.GET.get("employee_code", "").strip()
    from_date = request.GET.get("from_date", "").strip()
    to_date = request.GET.get("to_date", "").strip()
    paid_filter = request.GET.get("paid", "").strip()

    payrolls = Payroll.objects.filter(company_id=company_id).select_related("employee").order_by("-date")

    if employee_name:
        payrolls = payrolls.filter(
            employee__first_name__icontains=employee_name
        ) | payrolls.filter(
            employee__last_name__icontains=employee_name
        )

    if employee_code:
        payrolls = payrolls.filter(employee__employee_code__icontains=employee_code)

    if from_date:
        payrolls = payrolls.filter(date__gte=from_date)

    if to_date:
        payrolls = payrolls.filter(date__lte=to_date)

    if paid_filter == "yes":
        payrolls = payrolls.filter(paid=True)
    elif paid_filter == "no":
        payrolls = payrolls.filter(paid=False)

    # Default: hide paid payrolls from the main screen
    if not employee_name and not employee_code and not from_date and not to_date and not paid_filter:
        payrolls = payrolls.filter(paid=False)

    payrolls = payrolls.distinct().order_by("-date")

    return render(request, "payroll/payroll_list.html", {
        "payrolls": payrolls,
        "company_name": company_name,
        "employee_name": employee_name,
        "employee_code": employee_code,
        "from_date": from_date,
        "to_date": to_date,
        "paid_filter": paid_filter,
    })


@login_required
def payroll_create(request):
    company_id = request.session.get("company_id")
    company = Company.objects.get(id=company_id)

    if request.method == "POST":
        form = PayrollForm(request.POST, company_id=company_id)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.company = company
            payroll.save()
            return redirect("payroll_list")
    else:
        form = PayrollForm(company_id=company_id)

    return render(request, "payroll/payroll_form.html", {
        "form": form,
        "title": "Add Payroll",
        "company_name": request.session.get("company_name"),
    })


@login_required
def payroll_update(request, pk):
    company_id = request.session.get("company_id")
    payroll = get_object_or_404(Payroll, pk=pk, company_id=company_id)

    if request.method == "POST":
        form = PayrollForm(request.POST, instance=payroll, company_id=company_id)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.save()
            return redirect("payroll_list")
    else:
        form = PayrollForm(instance=payroll, company_id=company_id)

    return render(request, "payroll/payroll_form.html", {
        "form": form,
        "title": "Edit Payroll",
        "company_name": request.session.get("company_name"),
    })


@login_required
def payroll_delete(request, pk):
    company_id = request.session.get("company_id")
    payroll = get_object_or_404(Payroll, pk=pk, company_id=company_id)

    if request.method == "POST":
        payroll.delete()
        return redirect("payroll_list")

    return render(request, "payroll/payroll_confirm_delete.html", {"payroll": payroll})


@login_required
def payroll_print(request, pk):
    company_id = request.session.get("company_id")
    payroll = get_object_or_404(Payroll, pk=pk, company_id=company_id)

    if not payroll.paid:
        payroll.paid = True
        payroll.paid_date = timezone.now().date()
        payroll.save()

    return render(request, "payroll/payroll_print.html", {
        "payroll": payroll,
        "company_name": request.session.get("company_name"),
    })
