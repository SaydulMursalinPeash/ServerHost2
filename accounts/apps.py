from django.apps import AppConfig
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2P.settings')

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    def ready(self) -> None:
        import django
        django.setup()
        