import os
import django
import io
from django.core.management import call_command

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "captainmedia.settings")
django.setup()

# Dump data using UTF-8 encoding to handle emojis
with io.open("data.json", "w", encoding="utf-8") as f:
    call_command(
        "dumpdata",
        "--natural-primary",
        "--natural-foreign",
        "--exclude", "auth.permission",
        "--exclude", "contenttypes",
        stdout=f
    )

print("✅ Data successfully exported to data.json with UTF-8 encoding.")
