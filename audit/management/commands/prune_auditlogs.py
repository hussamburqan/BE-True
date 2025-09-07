from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from audit.models import AuditLog

class Command(BaseCommand):
    help = "Delete old audit logs (default 7 days)."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=getattr(settings, "AUDITLOG_RETENTION_DAYS", 7))

    def handle(self, *args, **opts):
        days = int(opts["days"])
        cutoff = timezone.now() - timedelta(days=days)
        qs = AuditLog.objects.filter(created_at__lt=cutoff)
        count = qs.count()
        qs.delete()
        self.stdout.write(self.style.SUCCESS(f"Pruned {count} audit logs older than {days} days."))
