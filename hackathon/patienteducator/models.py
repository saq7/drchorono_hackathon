from __future__ import unicode_literals
import os

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Patient(models.Model):
    # all optional POST fields in the drchrono api are optional
    drchrono_id = models.IntegerField()
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=25, null=True)
    race = models.CharField(max_length=50, null=True)
    drchrono_doctor_id = models.IntegerField()
    user = models.ForeignKey(User)

    @property
    def name(self):
        name = self.first_name + ' ' + self.last_name
        return name.title()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/patient_<id>/<filename>
    return 'user_{0}/patient_{1}/{2}'.format(instance.user.id, instance.patient.id,  filename)


class Document(models.Model):
    docfile = models.FileField(upload_to=user_directory_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return os.path.basename(self.docfile.name)


class UserPatientDocsURL(models.Model):
    shortened_url = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'patient',)
