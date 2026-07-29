import os
import django
import dj_database_url

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Point Django to Render PostgreSQL if DATABASE_URL is set
database_url = os.environ.get("DATABASE_URL")
if database_url:
    os.environ["DATABASE_URL"] = database_url

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "skyblue"
email = "unninair@gmail.com"
password = "Skyblue@12345"

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        "email": email,
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
    },
)

user.email = email
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.set_password(password)
user.save()

if created:
    print(f"Created user: {username}")
else:
    print(f"Updated user: {username}")
