from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


class Command(BaseCommand):
    help = "Deletes expired tokens from the database (outstanding + blacklisted)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many tokens would be deleted without actually deleting them",
        )

    def handle(self, *args, **options):
        now = timezone.now()
        expired_qs = OutstandingToken.objects.filter(expires_at__lt=now)
        count = expired_qs.count()

        if options["dry_run"]:
            self.stdout.write(f"[dry-run] Would delete {count} expired token(s).")
            return

        expired_qs.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} expired token(s)."))
