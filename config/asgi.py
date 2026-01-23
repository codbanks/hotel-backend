import os
from django.core.asgi import get_asgi_application

# 1. Set the settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. Get the ASGI application (this handles your urls.py automatically)
django_asgi_app = get_asgi_application()

# 3. Simple application export
# This tells Render: "Just handle HTTP requests using my standard URLs"
application = django_asgi_app