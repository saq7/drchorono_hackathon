from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Patient(models.Model):
    # all optional POST fields in the drchrono api are optional
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=25, null=True)
    race = models.CharField(max_length=50, null=True)
    photo = models.FileField(null=True)
    doctor = models.ForeignKey(User)


class Document(models.Model):
    doctor = models.ForeignKey(User, on_delete='cascade')
    patient = models.ForeignKey(Patient, on_delete='cascade')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
