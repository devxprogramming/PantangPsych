from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Patient(models.Model):

    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('rather not say', 'Rather not say')
    )

    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER)
    contact_info = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role__in': ['doctor', 'admin']})
    created_at = models.DateTimeField(auto_now_add=True)