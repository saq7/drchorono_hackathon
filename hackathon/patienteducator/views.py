from datetime import date, timedelta
from datetime import datetime
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from models import Patient, Document
from forms import EducationalDocumentForm
from helpers import get_appointments
from helpers import create_appt_dict
from helpers import get_bitly_url
from urlparse import urlparse


def index(request):
    if request.user.is_authenticated():
        appointments = get_appointments(
            request.session['access_token']
        )
        appointments = create_appt_dict(appointments)
        return render(request, 'patienteducator/index.html',
                      {'appointments': appointments})
    else:
        return render(request, 'patienteducator/index.html')


def patient_documents(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    user = request.user
    # Handle file upload
    if request.method == 'POST':
        form = EducationalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = Document(docfile=request.FILES['docfile'])
            doc.patient = patient
            doc.user = request.user
            doc.save()

    form = EducationalDocumentForm()  # An empty, unbound form
    # bitly does not shorten localhost links
    parsed_url = urlparse(request.build_absolute_uri())
    longurl = parsed_url.scheme + '://' + parsed_url.netloc
    longurl += '/patient_share/user/' + str(user.id) + '/patient/' + patient_id
    shortened_url = get_bitly_url(
        longurl,
        user,
        patient
    )
    if shortened_url:
        url_to_share = shortened_url
    else:
        url_to_share = longurl

    # Load documents for the list page
    documents = Document.objects.filter(user=user, patient=patient)
    return render(request, 'patienteducator/patient.html',
                  {'documents': documents,
                   'form': form,
                   'patient': patient,
                   'shortened_url': url_to_share})


def share_documents(request, user_id, patient_id):
    # when a patient goes to this view, they are
    # able to see whatever their doctor uploaded
    # url: /user/:id/patient/:id
    docfiles = Document.objects.filter(
        user_id=user_id, patient_id=patient_id)
    patient = Patient.objects.get(id=patient_id)
    return render(request, 'patienteducator/patient_share.html',
                  {'documents': docfiles,
                   'patient': patient})
