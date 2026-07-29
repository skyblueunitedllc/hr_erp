from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Reset password for the live admin user"

    def handle(self, *args, **options):
        username = "skyblueunitedllc"
        new_password = "Butterfly@11002"
        email = "unniarms@gmail.com"

        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(new_password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created user {username}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Reset password for {username}"))
