#!/usr/bin/env python
"""Script to fix portfolio database issues."""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/mrdev02/Documents/ECOMM_DEV')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommdev.settings')
django.setup()

from django.db import connection

# Drop the tags table if it exists (it was created incorrectly)
with connection.cursor() as cursor:
    try:
        cursor.execute("DROP TABLE IF EXISTS portfolio_case_tags CASCADE;")
        print("✓ Dropped portfolio_case_tags table")
    except Exception as e:
        print(f"Note: {e}")

# Delete all CaseImages (they reference cases)
from portfolio.models import CaseImage, Case, CategoriaPortfolio, Tag

try:
    count = CaseImage.objects.all().delete()
    print(f"✓ Deleted CaseImages: {count}")
except Exception as e:
    print(f"Error deleting CaseImages: {e}")

# Delete all Cases
try:
    count = Case.objects.all().delete()
    print(f"✓ Deleted Cases: {count}")
except Exception as e:
    print(f"Error deleting Cases: {e}")

# Delete all Categories
try:
    count = CategoriaPortfolio.objects.all().delete()
    print(f"✓ Deleted Categories: {count}")
except Exception as e:
    print(f"Error deleting Categories: {e}")

# Delete all Tags
try:
    count = Tag.objects.all().delete()
    print(f"✓ Deleted Tags: {count}")
except Exception as e:
    print(f"Error deleting Tags: {e}")

print("\n✓ Portfolio database cleaned!")
print("You can now add new cases from the admin panel.")
