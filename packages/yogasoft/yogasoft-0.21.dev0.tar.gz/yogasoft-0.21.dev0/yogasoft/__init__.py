from __future__ import absolute_import, unicode_literals
import os
import sys

from .celery import app as celery_app
__all__ = ['celery_app']


def manage():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yogasoft.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
