from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_superuser(apps, schema_editor):
    User = apps.get_model("auth", "User")

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


def remove_superuser(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="skyblue").delete()


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunPython(create_superuser, remove_superuser),
    ]
