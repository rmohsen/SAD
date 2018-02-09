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


class Transaction(models.Model):
    issue_tracking_number = models.IntegerField()


class Position(models.Model):
    accountant_phases = models.ForeignKey(Phase, on_delete=models.CASCADE)


class Process(models.Model):
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
