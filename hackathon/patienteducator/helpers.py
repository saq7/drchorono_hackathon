from datetime import datetime, date, timedelta
import requests
import urllib
from urlparse import urlparse
from models import Patient
from models import UserPatientDocsURL


# TODO: move to env var
drchrono_base_url = 'https://drchrono.com/api'
patients_url = '/patients'


def get_appointments(access_token):
    today = date.today()
    yesterday = str(today - timedelta(days=1))
    tomorrow = str(today + timedelta(days=2))
    appt_range = yesterday + '/' + tomorrow
    appointments_url = drchrono_base_url + '/appointments'
    appointments = []
    while appointments_url:
        data = requests.get(
            appointments_url,
            params={'date_range': appt_range},
            headers={'Authorization': 'Bearer %s' % access_token}
        ).json()
        appointments.extend(data['results'])
        appointments_url = data['next']
    return appointments


def create_appt_dict_for_user(appointments, user, access_token):
    appt_dict = {'today': [], 'yesterday': [],
                 'tomorrow': [], 'day_after_tomorrow': []}
    for appt in appointments:
        patient = get_patient_for_user(appt, user, access_token)
        appt_time = appt['scheduled_time']
        appt_time = datetime.strptime(appt_time, '%Y-%m-%dT%H:%M:%S')
        day = which_day(appt_time)
        appt_dict[day] += [(patient, str(appt_time))]
    return appt_dict


def which_day(_datetime):
    if _datetime.date() == date.today():
        return 'today'
    if _datetime.date() == date.today() - timedelta(days=1):
        return 'yesterday'
    if _datetime.date() == date.today() + timedelta(days=1):
        return 'tomorrow'
    if _datetime.date() == date.today() + timedelta(days=2):
        return 'day_after_tomorrow'


def get_patient_for_user(appt, user, access_token):
    patient = appt['patient']
    p = None
    try:
        p = Patient.objects.get(drchrono_id=patient)
    except Patient.DoesNotExist:
        patient_uri = drchrono_base_url + patients_url + '/' + str(patient)
        patient_data = requests.get(
            patient_uri,
            headers={'Authorization': 'Bearer %s' % access_token}
        ).json()
        p = Patient()
        p.drchrono_id = patient
        p.first_name = patient_data.get('first_name')
        p.last_name = patient_data.get('last_name')
        p.email = patient_data.get('email')
        p.gender = patient_data.get('gender')
        p.race = patient_data.get('race')
        p.photo = patient_data.get('photo')
        p.drchrono_doctor_id = patient_data.get('doctor')
        p.user_id = user.id
        p.save()
    return p


def get_bitly_url(request, user, patient):
    # TODO: move bitly_token and bitly_base to env vars
    try:
        url = UserPatientDocsURL.objects.get(
            user=user, patient=patient)
        return url.shortened_url
    except UserPatientDocsURL.DoesNotExist:
        parsed_url = urlparse(request.build_absolute_uri())
        longurl = parsed_url.scheme + '://' + parsed_url.netloc
        longurl += '/patient_share/user/' + \
            str(user.id) + '/patient/' + str(patient.id)  # HACK!
        bitly_token = 'ffe71e89efdbfbb4d03a4995a7910cd4e8416ba7'
        bitly_base = 'https://api-ssl.bitly.com/v3/shorten'
        response = requests.get(bitly_base, params={
            'access_token': bitly_token,
            'longUrl': urllib.quote(longurl, safe=''),
            'format': 'json'
        }).json()
        if response['status_code'] != 200:
            return longurl
        else:
            shortened_url = response['data']
            UserPatientDocsURL(
                user=user,
                patient=patient,
                shortened_url=shortened_url
            ).save()
            return shortened_url
