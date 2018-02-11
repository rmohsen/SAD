from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Transaction(models.Model):
    issue_tracking_number = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    amount = models.IntegerField(default=0)
    account_id = models.ForeignKey(User, on_delete=models.CASCADE,default=None)


class Attachment(models.Model):
    title = models.CharField(max_length=10)
    file = models.FileField(default=None)


class Position(models.Model):
    title = models.CharField(max_length=10)


class PhaseType(models.Model):
    accountant_position = models.ManyToManyField(Position)
    attachments = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


class Phase(models.Model):
    phase_type = models.ForeignKey(PhaseType, on_delete=models.CASCADE)
    next_phase_acc = models.IntegerField(default=0)  # next_phase_id
    next_phase_rej = models.IntegerField(default=0)
    start_time = models.DateField(default=timezone.now)
    finish_time = models.DateField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=False)


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=None)
    birth_date = models.DateField(default=timezone.now)
    identity_code = models.CharField(max_length=10, primary_key=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=None)
    identity_code = models.CharField(max_length=10, default="")
    birth_date = models.DateField(default=timezone.now)
    level = models.CharField(max_length=10, default="")
    student_number = models.CharField(max_length=10, default="")
    id = models.IntegerField(default=0, primary_key=True)


class ProcessType(models.Model):
    name = models.CharField(max_length=10, unique=True, default="")
    # phases = models.ForeignKey(Phase, on_delete=models.CASCADE)
    start_phase = models.OneToOneField(Phase, on_delete=models.CASCADE)


class Process(models.Model):
    start_time = models.TimeField(default=timezone.now)
    finish_time = models.TimeField(default=timezone.now)
    process_type = models.ForeignKey(ProcessType, on_delete=models.CASCADE)
    student_owner = models.ForeignKey(Student, on_delete=models.CASCADE)
