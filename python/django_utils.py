##################################################
#
#   Author          : josuebrunel
#   Filename        : django.py
#   Description     :
#   Creation Date   : 21-10-2015
#   Last Modified   : Tue 26 Jan 2016 08:52:22 AM CET
#
##################################################

import os
import imp
import logging

def load_common(common):
    """loads dj_common.py
    """
    return imp.load_source('common', common)

if os.environ.get('DJANGO_SETTINGS_MODULE', None):
     
    logging.info("LOADING DJANGO UTILS")

    from django.conf import settings
    from django.db import models
    from django.contrib.auth import get_user_model
    from django.core.urlresolvers import reverse, resolve
    from django.shortcuts import get_object_or_404, render, resolve_url

    from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

    # If django configured 
    if settings.configured:
        User = get_user_model()

        users = User.objects.all()

        # Allows you to import whatever you need for you current django
        # when lunching shell
        django_common = os.path.join(
            os.path.realpath('.'), 'dj_common.py'
        )
        if os.path.exists(django_common):
            common = load_common(django_common)
            from common import *




