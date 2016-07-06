import re
import requests
from django.contrib.auth.models import User


def get_referer_view(request, default=None):
    # if the user typed the url directly in the browser's address bar
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    if referer[0] != request.META.get('SERVER_NAME'):
        return default

    # add the slash at the relative path's view and finished
    referer = u'/' + u'/'.join(referer[1:])
    return referer


def get_drchrono_user(request):
    # get the current user from the api
    uri = 'https://drchrono.com/api/users/current'
    # TODO: move the uri above to a centralized location of api strings
    response = requests.get(uri, headers={
        'Authorization': 'Bearer %s' % request.session['access_token'],
    })
    user_data = response.json()

    # get the doctor object from the api
    doctor_uri = user_data['doctor']
    uri = 'https://drchrono.com/api/doctors/' + str(doctor_uri)
    response = requests.get(uri, headers={
        'Authorization': 'Bearer %s' % request.session['access_token'],
    })
    doctor_data = response.json()

    # retrieve/create user from/in database
    try:
        user = User.objects.get(username=user_data['username'])
        return user
    except User.DoesNotExist:
        user = User.objects.create_user(user_data['username'])
        user.first_name = doctor_data['first_name']
        user.last_name = doctor_data['last_name']
        user.email = doctor_data['email']
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save()
        return user
