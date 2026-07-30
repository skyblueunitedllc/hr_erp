from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from .models import Company


@login_required
def select_company(request):
    profile = getattr(request.user, "userprofile", None)

    # Super admin sees all active companies
    if profile and profile.role == "super_admin":
        companies = Company.objects.filter(is_active=True)
    # Company admin / staff sees only their own company
    elif profile and profile.company:
        companies = Company.objects.filter(id=profile.company.id, is_active=True)
    # No company assigned: show nothing
    else:
        companies = Company.objects.none()

    if request.method == "POST":
        if "create_company" in request.POST:
            # Only super admin should be able to create companies
            if not profile or profile.role != "super_admin":
                return redirect("select_company")

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
            return redirect("/report/dashboard/")

        company_id = request.POST.get("company_id")
        company = Company.objects.filter(id=company_id, is_active=True).first()

        if company:
            # Company users can only select their own company unless super admin
            if profile and profile.role == "super_admin":
                request.session["company_id"] = company.id
                request.session["company_name"] = company.name
                return redirect("/report/dashboard/")

            if profile and profile.company and profile.company.id == company.id:
                request.session["company_id"] = company.id
                request.session["company_name"] = company.name
                return redirect("/report/dashboard/")

    return render(request, "companies/select_company.html", {"companies": companies})
