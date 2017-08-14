"""
WSGI config for apiserver project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
paths =["/var/www/apiserver"]
for path in paths:
    if path not in sys.path:
        sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiserver.settings")

application = get_wsgi_application()
