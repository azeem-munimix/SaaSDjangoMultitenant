from django.db import models
from django.contrib.auth.models import AbstractUser


class CoreUser(AbstractUser):
    """Custom user able to act as a global core user."""

    is_core = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return self.username


# Add additional global models here
