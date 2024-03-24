from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required for creating a user.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'authentication'

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest implementation: all permissions are granted to a superuser
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app app_label?"
        # Simplest implementation: all permissions are granted to a superuser
        return self.is_active and self.is_superuser


class Rack(models.Model):
    rack_number = models.CharField(max_length=100, unique=True)

    def _str_(self):
        return self.rack_number

class Target(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    number = models.CharField(max_length=100)
    telnet_port = models.CharField(max_length=100)
    telnet_id = models.CharField(max_length=100)
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('rack', 'number')

    def _str_(self):
        return f"{self.rack.rack_number} - {self.number}"