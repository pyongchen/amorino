"""
WSGI config for glasses_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, '..', 'site-packages'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glasses_project.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
