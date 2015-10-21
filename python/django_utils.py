##################################################
#
#   Author          : josuebrunel
#   Filename        : django.py
#   Description     :
#   Creation Date   : 21-10-2015
#   Last Modified   : Wed 21 Oct 2015 02:32:48 PM CEST
#
##################################################

import os
import logging

if os.environ.get('DJANGO_SETTINGS_MODULE', None):
    
    logging.info("LOADING DJANGO UTILS")

    from django.contrib.auth import get_user_model

    User = get_user_model()

    users = User.objects.all()
