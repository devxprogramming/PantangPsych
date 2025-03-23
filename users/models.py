from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, *args, **kwargs):
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, *args, **kwargs):
        user = self.create_user(email, first_name, last_name, password, *args, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('nurse', 'Nurse'),
        ('doctor', 'Doctor'),
        ('consultant', 'Consultant'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=20, default='nurse')