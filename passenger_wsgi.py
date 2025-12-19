# /home/sandhan1/api.sandhanishsmcu.com/passenger_wsgi.py
import os, sys

PROJECT_ROOT = "/home/sandhan1/api.sandhanishsmcu.com"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Make sure this matches your project package name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suhrawardy_medical.settings")

from suhrawardy_medical.wsgi import application  # uses the wsgi.py in your project
