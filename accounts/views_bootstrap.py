from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import HttpResponse

def bootstrap_render_user(request):
    User = get_user_model()

    username = "skyblue"
    email = "unninair@gmail.com"
    password = "Skyblue@12345"

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "password": make_password(password),
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        },
    )

    if not created:
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.password = make_password(password)
        user.save()

    return HttpResponse("Bootstrap user created or updated.")
