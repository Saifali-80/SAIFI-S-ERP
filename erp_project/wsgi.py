import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')

application = get_wsgi_application()

# For Vercel deployments using SQLite (no DATABASE_URL):
# Run migrations at startup since /tmp is ephemeral across function instances
import sys
if 'migrate' not in sys.argv:
    try:
        from django.conf import settings
        if settings.DATABASE_URL is None and getattr(settings, 'VERCEL', False):
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
                if cursor.fetchone() is None:
                    from django.core.management import call_command
                    call_command('migrate', '--noinput', '--verbosity', '0')
    except Exception:
        pass