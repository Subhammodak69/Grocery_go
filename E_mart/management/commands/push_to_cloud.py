from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connections
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Push ALL data from local DB → Cloud (Render) DB'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Preview only')
        parser.add_argument('--models', nargs='+', help='Specific models e.g. store.category store.product')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        specific_models = options.get('models')

        # Test both connections
        for alias, label in [('local', 'Local'), ('default', 'Cloud')]:
            try:
                connections[alias].ensure_connection()
                self.stdout.write(self.style.SUCCESS(f'✅ {label} DB connected'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ {label} DB unavailable: {e}'))
                return

        total_pushed = 0
        models_pushed = []
        SKIP_APPS = ['auth', 'contenttypes', 'admin', 'sessions']

        for model in apps.get_models():
            try:
                model_name = f"{model._meta.app_label}.{model._meta.model_name}"

                if model._meta.app_label in SKIP_APPS:
                    continue

                if specific_models and model_name not in specific_models:
                    continue

                # Fetch from LOCAL
                local_data = list(model.objects.using('local').values())

                if not local_data:
                    self.stdout.write(f"⏭️  {model_name}: no local data, skipping")
                    continue

                if dry_run:
                    self.stdout.write(f"📋 {model_name}: {len(local_data)} records (dry run)")
                    continue

                # Clear cloud data for this model
                model.objects.using('default').all().delete()

                # Push to cloud
                cloud_objects = [model(**data) for data in local_data]
                model.objects.using('default').bulk_create(cloud_objects, ignore_conflicts=True)

                total_pushed += len(local_data)
                models_pushed.append(f"{model_name} ({len(local_data)})")
                self.stdout.write(self.style.SUCCESS(f"✅ {model_name}: {len(local_data)} records pushed"))

            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️  {model_name}: {e}"))
                continue

        self.stdout.write(self.style.SUCCESS(f"\n🚀 PUSH COMPLETE!"))
        self.stdout.write(f"📊 Total records pushed: {total_pushed}")
        self.stdout.write(f"📋 Models: {', '.join(models_pushed)}")