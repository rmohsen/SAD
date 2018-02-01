from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    identity_code = models.CharField(max_length=10, primary_key=True)
    birth_date = models.DateField()

from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birth_date = models.DateField()

class Attachment(models.Model):
    title = models.CharField()
    file = models.FileField()

class Transaction(models.Model):
    pass

class Position(models.Model):
    accountant_phases = models.ForeignKey(Phase)
    pass

class Process(models.Model):
    phases = models.ForeignKey(Phase)
    start_phase = models.OneToOneField(Phase)
    pass

class Phase(models.Model):
    phase_type = models.ForeignKey(PhaseType)
    next_phase_acc = models.OneToOneField(Phase)
    next_phase_rej = models.OneToOneField(Phase)
    is_verified = models.BooleanField()
    pass

class PhaseType(models.Model):
    accountent_position = models.ManyToManyField(Position)
    # attachments =
    # transaction
    pass

