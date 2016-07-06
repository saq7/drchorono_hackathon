from datetime import date, timedelta
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# need views for
# - welcome with login
# - logged in page, with list of appointments
# - patient page,
# -- with control to add documents,
# -- see list of previously added documents,
# -- and checkboxes to select documents to share,
# -- and share button to share selected documents

# TODO: move to env var
drchrono_base_url = 'https://drchrono.com/api'


def index(request):
    if request.user.is_authenticated():
        # show logged in page
        # with a list of patients
        # each patient should have an expandable details
        # each patient should be clickable
        # clicking the patient should take you to that

        # the appointments call should be made here
        # once the call is made, all patients not in db
        # need to be retrieved with another api call

        # first make a call for the appointments

        today = date.today()
        yesterday = str(today - timedelta(days=1))
        tomorrow = str(today + timedelta(days=1))
        appt_range = yesterday + '/' + tomorrow
        appointments_url = drchrono_base_url + '/appointments'
        appointments = []
        while appointments_url:
            data = requests.get(
                appointments_url,
                params={'date_range': appt_range},
                headers={'Authorization': 'Bearer %s' % request.session[
                    'access_token']}
            ).json()
            appointments.extend(data['results'])
            appointments_url = data['next']
        # return HttpResponse(json.dumps(appointments))
        return render(request, 'patienteducator/index.html',
                      {'appointments': appointments})
    #{'appointments': appointments})
    else:
        # show non logged in welcome page
        # return HttpResponse('user not authenticated')
        return render(request, 'patienteducator/index.html')


def patients(request):
    # arrive here after a doctor has clicked a patient
    # make an api call to get documents shared with that
    # patient

    pass


def document(request):
    # when the doctor adds a file, make a post ajax request
    # upload documents here
    pass


def share_documents(request):
    # when the doctor makes a post request here
    # the ids of the documents to be shared will be
    # delivered along with the id of the patient
    # create a celery task
    pass
