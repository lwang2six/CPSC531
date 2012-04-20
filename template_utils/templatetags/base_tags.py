import os
import Image

from django.template import Library
from django.conf import settings

register = Library()

def URL_PREFIX():
    return settings.URL_PREFIX
register.simple_tag(URL_PREFIX)

def STATIC_PREFIX():
    return settings.STATIC_PREFIX
register.simple_tag(STATIC_PREFIX)
