import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

activate_this = os.path.join(BASE_DIR, "venv", "bin", "activate_this.py")
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {"__file__": activate_this})

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suhrawardy_medical.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
