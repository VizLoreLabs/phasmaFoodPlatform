from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import CharField, EmailField, ForeignKey, SET_NULL
from django.utils.translation import ugettext_lazy as _
from typing import Dict

class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    """
    def create_user(self, email: str, password: str, **extra_fields: dict):
        """Create and save a User with the given email and password."""

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Dict[str, bool]):
        """Create and save a SuperUser with the given email and password."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model, extended Django base user with some extra fields."""
    username = None
    email = EmailField(_("email address"),
                       max_length=254,
                       db_index=True,
                       unique=True,
                       help_text=_("Type Your email address")
                       )
    company = CharField(_("company"),
                        max_length=127,
                        default="OTHER",
                        help_text=_("Choose company name.")
                        )
    user_type = CharField(_("user type"),
                          max_length=127,
                          default="BASIC",
                          help_text=_("User type defines access.")
                          )
    phasma_device = ForeignKey("devices.PhasmaDevice",
                               on_delete=SET_NULL,
                               null=True,
                               help_text=_("Phasma device used during measurement."),
                               related_name="users"
                               )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.email
