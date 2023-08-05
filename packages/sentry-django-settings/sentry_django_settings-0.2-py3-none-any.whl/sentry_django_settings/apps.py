"""
This is the Django configuration file for Sentry.
"""
from __future__ import unicode_literals
import logging

from django.apps import AppConfig
from django.conf import settings

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import git


logger = logging.getLogger("django.sentry_django_settings")


class Sentry(AppConfig):
    name = 'sentry_django_settings'

    def ready(self):
        if not getattr(settings, "SENTRY"):
            logger.warning("No SENTRY settings found.")
            return
        if not settings.SENTRY["enabled"]:
            logger.info("Sentry disabled.")
            return

        self.init_sentry(settings.SENTRY['dsn'], settings.SENTRY['environment'])
        logger.info("Sentry enabled.")

    def init_sentry(self, dsn, environment):
        """
        Sets up Sentry to send errors to the Sentry server.
        """
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha

        sentry_sdk.init(
            dsn=dsn,
            integrations=[DjangoIntegration()],
            environment=environment,
            release=sha,
        )
