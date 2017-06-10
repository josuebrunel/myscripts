import os


if os.environ.get('DJANGO_SETTINGS_MODULE', None):

    logger.info("LOADING DJANGO UTILS")

    from django.conf import settings
    from django.apps.registry import apps
    from django.core.cache import cache

    def clear_cache():
        cache.clear()

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
            logger.info("LOADING DJANGO_COMMON FILE")
            execfile(django_common)
