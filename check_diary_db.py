# check_diary_db.py

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WD.settings')  # 🔁 Replace with your actual project name
django.setup()

from diaryapp.models import DiaryEntry

# Determine DB alias used for reading
from django.db import router

db = router.db_for_read(DiaryEntry)
print(f"📦 Django is using the '{db}' database for DiaryEntry (read operations).")

# Confirm DB file path (if using SQLite)
from django.conf import settings
db_settings = settings.DATABASES[db]

if db_settings['ENGINE'] == 'django.db.backends.sqlite3':
    print(f"📄 That maps to SQLite file: {db_settings['NAME']}")
else:
    print(f"⚠️ Non-SQLite DB engine detected: {db_settings['ENGINE']}")
