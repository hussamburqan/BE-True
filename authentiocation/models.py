from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, tel_number, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not tel_number:
            raise ValueError("Users must have a phone number")
        extra_fields.setdefault('is_staff', True)

        email = self.normalize_email(email).lower().strip()

        user = self.model(
            email=email,
            tel_number=tel_number,
            name=name,
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, tel_number, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, tel_number, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    tel_number = models.CharField(max_length=20, unique=True)
    name       = models.CharField(max_length=255)
    email      = models.EmailField(max_length=255, unique=True)

    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name', 'tel_number']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.name} <{self.email}>"
