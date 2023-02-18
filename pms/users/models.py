from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .managers import CustomUserManager

# Create your models here.


class UserMaster(AbstractUser):
    ADMIN = "admin"
    USER = "user"

    USER_TYPE = (
        (ADMIN, "Admin"),
        (USER, "User"),
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        blank=True,
        default="",
    )
    email = models.EmailField(_("email address"), unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
