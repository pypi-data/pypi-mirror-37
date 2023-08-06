import unittest
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse

from django import middleware

