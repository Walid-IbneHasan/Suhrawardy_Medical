# dump_sqlite.py
import os
import django
from django.core.management import call_command

# make sure this matches your project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suhrawardy_medical.settings")

# Force UTF-8 writes on Windows
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

django.setup()

with open("data.json", "w", encoding="utf-8", newline="\n") as f:
    call_command(
        "dumpdata",
        use_natural_primary_keys=True,
        use_natural_foreign_keys=True,
        exclude=[
            "contenttypes",
            "auth.permission",
            "admin.logentry",
            "sessions.session",
        ],
        indent=2,
        stdout=f,
    )

print("Wrote data.json")
