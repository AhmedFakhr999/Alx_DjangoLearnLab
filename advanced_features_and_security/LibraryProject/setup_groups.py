
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

def setup_groups():
    # Define permissions
    try:
        content_type = ContentType.objects.get_for_model(Book)
    except Exception as e:
        print(f"Error getting content type: {e}")
        return

    permissions = {
        'can_view': Permission.objects.get(codename='can_view', content_type=content_type),
        'can_create': Permission.objects.get(codename='can_create', content_type=content_type),
        'can_edit': Permission.objects.get(codename='can_edit', content_type=content_type),
        'can_delete': Permission.objects.get(codename='can_delete', content_type=content_type),
    }

    # Create Groups
    groups = {
        'Viewers': ['can_view'],
        'Editors': ['can_view', 'can_create', 'can_edit'],
        'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
    }

    for group_name, perms in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Created group: {group_name}")
        else:
            print(f"Group already exists: {group_name}")
        
        for perm_name in perms:
            group.permissions.add(permissions[perm_name])
            print(f"Added {perm_name} to {group_name}")

if __name__ == "__main__":
    setup_groups()
