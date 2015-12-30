import os
import sys

path = '/home2/jcm/django/newsletter/..'
if path not in sys.path:
   sys.path.append(path)

path = '/home2/jcm/django/newsletter'
if path not in sys.path:
   sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'newsletter.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
