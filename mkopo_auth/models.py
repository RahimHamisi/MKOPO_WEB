from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES=(
        ('admin','admin'),
        ('collector','collector'),
        ('client','client')
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number=models.CharField(max_length=15,unique=True,null=True,blank=True)
    address=models.TextField(blank=True,null=True)
    assigned_clients=models.ManyToManyField('self',
                                            symmetrical=False,
                                            related_name='collectors',
                                            blank=True,
                                            limit_choices_to={'role':'client'}
                                            )
    
    def __str__(self):
        return f"{self.username } with role of {self.role}"
