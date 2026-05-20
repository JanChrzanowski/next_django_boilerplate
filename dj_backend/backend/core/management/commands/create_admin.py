import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save


class Command(BaseCommand):
    help = (
        "Creates the admin superuser without a UserProfile record. "
        "Skips silently if the user already exists. "
        "Use --rotate-password to update the password of an existing admin."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--rotate-password",
            action="store_true",
            help="Update the admin password even if the user already exists",
        )

    def handle(self, *args, **options):
        from authentication.signals import create_user_profile

        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None:
            if options["rotate_password"]:
                user.set_password(password)
                user.save(update_fields=["password"])
                self.stdout.write(self.style.SUCCESS(f"Password rotated for '{username}'."))
            else:
                self.stdout.write(f"Admin '{username}' already exists — skipping.")
            return

        # Disconnect signal so no UserProfile row is created for the admin account
        post_save.disconnect(create_user_profile, sender=User)
        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created (no UserProfile)."))
        finally:
            post_save.connect(create_user_profile, sender=User)
