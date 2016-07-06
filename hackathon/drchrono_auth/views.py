from django.shortcuts import render, redirect
from rauth import OAuth2Service
from django.http import HttpResponse
import requests
# Create your views here.

# TODO: move these variables to env vars
client_id = 'JnXV8j2AF8S88MCcF8jcI0bRDIJM61MYBNDsKapl'
client_secret = 'kdbkci6ksn88Pnn8yeC2E5lPLks0CoT5VcGEP2h7h4d50YcueDioKdeqSc6Tm5CRmTt1DT7eWMgFmKCTP9enLqM3l12b1Flrek6ihEUZ2erz6M0iE9SfC0bg2wsFZiX6'
access_token_url = 'https://drchrono.com/o/token/'
authorize_url = 'https://drchrono.com/o/authorize/'
drchrono_base_url = 'https://drchrono.com/api/'
redirect_uri = 'http://127.0.0.1:8000/drchrono_auth/redirect'

# TODO: move this to services.py
drchrono_auth_service = OAuth2Service(
    name='drchrono',  # is this required?
    client_id=client_id,
    client_secret=client_secret,
    access_token_url=access_token_url,
    authorize_url=authorize_url,
    base_url=drchrono_base_url)


def index(request):
    # this view will be called when the user clicks on
    # login from the patienteducator app
    # the url params will consist of the required scopes

    # use the drchrono_auth_service to come up with
    # the redirect url with the required scopes

    scopes = request.GET.get('scopes')  # is a string
    params = {'redirect_uri': redirect_uri,
              'response_type': 'code',
              'scopes': scopes}
    drchrono_redirect_url = drchrono_auth_service.get_authorize_url(**params)
    return redirect(drchrono_redirect_url)


def redirect(request):
    # this is the view that will be called by the
    # drchrono api when it redirects the user

    # first get the code
    # create a dict with the request params
    # use the dict in a call to requests.post(token_url, dict)
    # save the return in response
    # call data = response.json
    # data should look like this
    # data = {'acces_token' : "fdhjkdfd",
    #         'refresh_token' : "fkjgfdlkj",
    #         'expires_in' : num_of_seconds
    #         .... misc keys and values}
    # once all of these are here and they work
    # save them in the database for the user who authorized

    code = request.GET.get('code')
    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(access_token_url, data=data)
    #resp_data = response.json()
    return HttpResponse(response)


# # rauth tutorial
# # params = {'redirect_uri': 'http://example.co',
# #           'response_type': 'code'}
# # url = service.get_authorize_url(**params)

# # # once the above URL is consumed by a client we can ask for an access
# # # token. note that the code is retrieved from the redirect URL above,
# # # as set by the provider
# # data = {'code': 'foobar',
# #         'grant_type': 'authorization_code',
# #         'redirect_uri': 'http://example.com/'}

# # session = service.get_auth_session(data=data)


# # step1
# # https://drchrono.com/o/authorize/?redirect_uri=REDIRECT_URI_ENCODED&response_type=code&client_id=CLIENT_ID_ENCODED&scope=SCOPES_ENCODED

# #step2
# # drchrono tutorial
# if 'error' in get_params:
#     raise ValueError('Error authorizing application: %s' % get_params[error])

# response = requests.post('https://drchrono.com/o/token/', data={
#     'code': get_params['code'],
#     'grant_type': 'authorization_code',
#     'redirect_uri': 'http://127.0.0.1:5000/drchrono_auth/redirect',
#     'client_id': 'JnXV8j2AF8S88MCcF8jcI0bRDIJM61MYBNDsKapl',
#     'client_secret': 'kdbkci6ksn88Pnn8yeC2E5lPLks0CoT5VcGEP2h7h4d50YcueDioKdeqSc6Tm5CRmTt1DT7eWMgFmKCTP9enLqM3l12b1Flrek6ihEUZ2erz6M0iE9SfC0bg2wsFZiX6',
# })
# response.raise_for_status()
# data = response.json()


# # Save these in your database associated with the user
# access_token = data['access_token']
# refresh_token = data['refresh_token']
# expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])
