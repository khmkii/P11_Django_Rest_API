"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from whitenoise.django import DjangoWhiteNoise

from django.core.wsgi import get_wsgi_application

path = "/home/khmkii/P11_Django_Rest_API/"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)