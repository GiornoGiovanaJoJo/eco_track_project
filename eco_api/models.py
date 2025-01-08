from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='the groups this user belongs to',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='specific permissions for this user',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions",
    )


class TransportType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EnergySource(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    energy_source = models.ForeignKey(EnergySource, on_delete=models.CASCADE)
    distance = models.FloatField()
    passengers = models.IntegerField()
    co2_emissions = models.FloatField(null=True, blank=True)
    other_emissions = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f"Trip from {self.start_date} to {self.end_date}"