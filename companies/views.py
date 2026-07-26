from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Company


@login_required
def select_company(request):
    companies = Company.objects.filter(is_active=True)

    if request.method == "POST":
        if "create_company" in request.POST:
            name = request.POST.get("name")
            code = request.POST.get("code")
            country = request.POST.get("country", "Oman")
            currency = request.POST.get("currency", "OMR")

            company = Company.objects.create(
                name=name,
                code=code,
                country=country,
                currency=currency,
                is_active=True,
            )
            request.session["company_id"] = company.id
            request.session["company_name"] = company.name
            return redirect("dashboard")

        company_id = request.POST.get("company_id")
        company = Company.objects.filter(id=company_id).first()

        if company:
            request.session["company_id"] = company.id
            request.session["company_name"] = company.name
            return redirect("dashboard")

    return render(request, "companies/select_company.html", {"companies": companies})
