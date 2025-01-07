from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='eco_api_user_groups',  # <- Здесь!
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='eco_api_user_permissions',  # <- Здесь!
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
class Trip(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    transport_type = models.CharField(max_length=100)
    distance = models.FloatField()
    route = models.JSONField() # Измените на models.JSONField
    passengers = models.PositiveIntegerField()
    energy_source = models.CharField(max_length=100)
    co2_emissions = models.FloatField()
    other_emissions = models.JSONField(default=dict) # Измените на models.JSONField

    def __str__(self):
        return f'Trip {self.id} ({self.transport_type})'