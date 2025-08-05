from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.files.storage import FileSystemStorage

# ⛔ Patch CloudinaryStorage BEFORE Django loads anything else
import sys
import types

# Fake cloudinary_storage module with dummy storage to avoid errors
class DummyCloudinaryStorage(FileSystemStorage):
    pass

# Patch import system so that when Cloudinary is imported, it returns dummy
sys.modules['cloudinary_storage.storage'] = types.ModuleType("cloudinary_storage.storage")
sys.modules['cloudinary_storage.storage'].MediaCloudinaryStorage = DummyCloudinaryStorage

# Patch CloudinaryField too if it exists
sys.modules['cloudinary_storage.models'] = types.ModuleType("cloudinary_storage.models")
sys.modules['cloudinary_storage.models'].MediaCloudinaryField = lambda *a, **kw: None

# Now continue with Django
from django.db.models.fields.files import FileField
import django
django.setup()


class Command(BaseCommand):
    help = "Safely loads data.json without needing Cloudinary credentials"

    def handle(self, *args, **options):
        print("🔧 Overriding all file storage with FileSystemStorage...")

        for model in self.get_all_models():
            for field in model._meta.get_fields():
                if isinstance(field, FileField):
                    field.storage = FileSystemStorage()

        print("📦 Loading data.json...")
        call_command('loaddata', 'data.json')
        print("✅ Data loaded successfully.")

    def get_all_models(self):
        from django.apps import apps
        return apps.get_models()
