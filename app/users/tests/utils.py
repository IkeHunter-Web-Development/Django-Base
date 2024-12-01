from users.models import User


def create_test_superuser(**kwargs):
    """Create Test Super User

    Used to create unique admin users quickly for testing, it will return
    admin user with test data.
    """
    email = "admin@example.com"
    password = "testpass"

    return User.objects.create_superuser(email=email, password=password, **kwargs)


def create_test_adminuser(**kwargs):
    """Create test admin/staff user."""
    email = "admin@example.com"
    password = "testpass"

    return User.objects.create_adminuser(email=email, password=password, **kwargs)
