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
    # get the referer_view and encode in the state param
    referer_view = get_referer_view(request, default='/')
    state = {'referer_view': referer_view}
    state = base64.b64encode(json.dumps(state))

    # get the scopes
    scopes = request.GET.get('scopes')  # is a string
    params = {'redirect_uri': redirect_uri,
              'response_type': 'code',
              'state': state,
              'scopes': scopes}
    drchrono_redirect_url = drchrono_auth_service.get_authorize_url(**params)
    return redirect(drchrono_redirect_url)


def redirect(request):
    # retrieve the view to redirect the user to
    state = request.GET.get('state')
    state = base64.b64decode(state)
    state = json.loads(state)
    referer_view = state['referer_view']

    if request.GET.get('error'):
        # if authentication error from drchrono
        # redirect back referer view
        return redirect(referer_view)
    else:
        # if authorization succeeded
        # get the access_token
        code = request.GET.get('code')
        token_dict = drchrono_auth_service.get_raw_access_token(
            data={'code': code,
                  'redirect_uri': redirect_uri,
                  'grant_type': 'authorization_code'})
        token_dict = token_dict.json()

        # add the access_token to the session, don't need refresh_token
        request.session[
            'access_token'] = token_dict.get('access_token')

        # get the user from db or create in db
        user = get_drchrono_user(request)

        # TODO: fortify the authentication backend being used
        # authenticate and login user
        user = authenticate(username=user.username,
                            token='currently, this token will always work')
        login(request, user)
        return redirect(referer_view)
