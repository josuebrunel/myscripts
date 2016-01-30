##################################################
#
#   Author          : josuebrunel
#   Filename        : django.py
#   Description     :
#   Creation Date   : 21-10-2015
#   Last Modified   : Sat 30 Jan 2016 12:13:11 PM CET
#
##################################################

import os
import imp
import logging

def load_common(common):
    """loads dj_common.py
    """
    try:
        module = imp.load_source('common', common)
        return module
    except (ImportError,) as e:
        logging.error(e)
        return None

if os.environ.get('DJANGO_SETTINGS_MODULE', None):

    logging.info("LOADING DJANGO UTILS")

    from django.core.exceptions import AppRegistryNotReady
    from django.conf import settings
    from django.apps.registry import apps

    # If django configured and apps ready
    if settings.configured and apps.apps_ready:
        from django.db import models
        from django.contrib.auth import get_user_model
        from django.core.urlresolvers import reverse, resolve
        from django.shortcuts import get_object_or_404, render, resolve_url
        from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

        User = get_user_model()

        users = User.objects.all()

        # Allows you to import whatever you need for you current django
        # when lunching shell
        django_common = os.path.join(
            os.path.realpath('.'), 'dj_common.py'
        )
        if os.path.exists(django_common):
            common = load_common(django_common)
            if common :
                from common import *

