from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from E_mart.constants.default_values import Role

class EMartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'E_mart'

    def ready(self):
        # Connect the create_admin function once after migrations
        post_migrate.connect(create_admin, sender=self)

def create_admin(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='Admin').exists():
        User.objects.create_superuser(
            username='Admin',
            first_name="Subham",
            last_name="Modak",
            email='modaksubham69@gmail.com',
            password='123456',
            role= Role.ADMIN.value
        )
