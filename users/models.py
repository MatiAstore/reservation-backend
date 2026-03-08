from django.contrib.auth.models import AbstractUser, Group 
from django.db import models

# Usert
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        STANDARD = 'STANDARD', 'Standard User'
        MAINTENANCE = 'MAINTENANCE', 'Mantenimiento'

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20, 
        choices= Role.choices,
        default= Role.STANDARD    
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role:
            group, _ = Group.objects.get_or_create(name=self.role)
            self.groups.add(group)

    def __str__ (self):
        return f"{self.username} - {self.get_role_display()}" 

