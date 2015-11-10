##################################################
#
#   Author          : josuebrunel
#   Filename        : django.py
#   Description     :
#   Creation Date   : 21-10-2015
#   Last Modified   : Tue 10 Nov 2015 06:37:54 PM CET
#
##################################################

import os
import logging

if os.environ.get('DJANGO_SETTINGS_MODULE', None):
    
    logging.info("LOADING DJANGO UTILS")

    from django.contrib.auth import get_user_model
    from djanog.core.urlresolvers import reverse as reverse
    from django.shortcuts import get_object_or_404, render, resolve_url

    User = get_user_model()

    users = User.objects.all()

    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'authentic2.settings':
        from authentic2.models import Service
        from django_rbac.utils import get_role_model
        Role = get_role_model()

        services = Service.objects.all()
        roles = Role.objects.all()



