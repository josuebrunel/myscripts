##################################################
#
#   Author          : josuebrunel
#   Filename        : django.py
#   Description     :
#   Creation Date   : 21-10-2015
#   Last Modified   : Thu 05 Nov 2015 04:48:12 PM CET
#
##################################################

import os
import logging

if os.environ.get('DJANGO_SETTINGS_MODULE', None):
    
    logging.info("LOADING DJANGO UTILS")

    from django.contrib.auth import get_user_model

    User = get_user_model()

    users = User.objects.all()

    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'authentic2.settings':
        from authentic2.models import Service
        from django_rbac.utils import get_role_model
        Role = get_role_model()

        services = Service.objects.all()
        roles = Role.objects.all()



