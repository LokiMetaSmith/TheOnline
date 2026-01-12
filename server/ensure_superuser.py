import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.insert(0, os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.conf.settings")
django.setup()

from evennia.accounts.models import AccountDB

def ensure_superuser():
    """
    Ensures a superuser exists. If Account #1 is missing, creates 'admin' with password 'admin'.
    """
    try:
        # Check if any account exists (usually #1 is the first one)
        if AccountDB.objects.count() == 0:
            print("No accounts found. Creating default superuser 'admin'...")
            # create_superuser is a method on the UserManager (AccountManager in Evennia)
            # Evennia's create_superuser takes key, email, password
            AccountDB.objects.create_superuser(
                key="admin",
                email="admin@localhost",
                password="admin"
            )
            print("Superuser 'admin' created successfully.")
        else:
            print("Accounts exist. Skipping superuser creation.")
    except Exception as e:
        print(f"Error checking/creating superuser: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ensure_superuser()
