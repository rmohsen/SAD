from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    identity_code = models.CharField(max_length=10, primary_key=True)
    birth_date = models.DateField()


# Create your models here.
