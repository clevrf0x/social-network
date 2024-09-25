from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class AppUserManager(BaseUserManager):
    """
    Custom manager for user models, providing methods to create standard users 
    and superusers based on email and password authentication.
    """
    
    def create_user(self, email: str, password: str, **extra_fields) -> 'AppUser':
        """
        Creates and saves a user with the given email and password.

        Args:
            email (str): The email address for the new user.
            password (str): The password for the new user.
            **extra_fields: Additional fields for user model customization.

        Returns:
            AppUser: The newly created user instance.

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> 'AppUser':
        """
        Creates and saves a superuser with the given email and password.

        Args:
            email (str): The email address for the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for user model customization.

        Returns:
            AppUser: The newly created superuser instance.

        Raises:
            ValueError: If is_staff or is_superuser are not set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
