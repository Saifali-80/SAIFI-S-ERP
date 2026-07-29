import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')

import django
django.setup()

# Run migrations on cold start (safe for PostgreSQL)
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'migrate', '--noinput'])

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
