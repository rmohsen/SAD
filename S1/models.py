from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    identity_code = models.CharField(max_length=10, primary_key=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


class Attachment(models.Model):
    title = models.CharField()
    file = models.FileField()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identity_code = models.CharField(max_length=10)
    birth_date = models.DateField()
    level = models.CharField(max_length=10)
    student_number = models.CharField(max_length=10)


class Transaction(models.Model):
    issue_tracking_number = models.IntegerField()
    date = models.DateField
    amount = models.IntegerField()
    account_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Position(models.Model):
    accountant_phases = models.ForeignKey(Phase, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)


class Process(models.Model):
    start_time = models.TimeField()
    finish_time = models.TimeField()
    process_type = models.ForeignKey(ProcessType, on_delete=models.CASCADE)
    student = models.ForeignKey(Student)


class ProcessType(models.Model):
    name = models.CharField(unique=True)
    # phases = models.ForeignKey(Phase, on_delete=models.CASCADE)
    start_phase = models.OneToOneField(Phase, on_delete=models.CASCADE)


class Phase(models.Model):
    phase_type = models.ForeignKey(PhaseType, on_delete=models.CASCADE)
    next_phase_acc = models.OneToOneField(PairPhase, on_delete=models.CASCADE)
    next_phase_rej = models.OneToOneField(PairPhase, on_delete=models.CASCADE)
    is_verified = models.BooleanField()
    is_finish = models.BooleanField()
    pass


class PairPhase(models.Model):
    f_phase = models.OneToOneField(Phase, on_delete=models.CASCADE)
    s_phase = models.OneToOneField(Phase, on_delete=models.CASCADE)
    is_acc = models.BooleanField()


class PhaseType(models.Model):
    accountent_position = models.ManyToManyField(Position)
    attachments = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
