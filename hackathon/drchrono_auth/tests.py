from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from . import views
# Create your tests here.

client = Client()
response = client.get(reverse(views.index))
