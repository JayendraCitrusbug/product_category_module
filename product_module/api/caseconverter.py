from rest_framework.settings import api_settings
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from rest_framework.utils import json
from rest_framework import renderers
from django.conf import settings
import codecs

def camel_to_snake(str):
    s = [str[0].lower()]
    for c in str[1:]:
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            s.append('_')
            s.append(c.lower())
        else:
            s.append(c)
    return ''.join(s)
