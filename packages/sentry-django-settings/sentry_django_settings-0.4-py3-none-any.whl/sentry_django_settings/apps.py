"""
This is the Django configuration file for Sentry.
"""
from __future__ import unicode_literals
import logging

from django.apps import AppConfig
from django.conf import settings

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from sentry_django_settings.git_sha import get_from_repo, get_from_file

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

        release = self.get_release()

        self.init_sentry(
            settings.SENTRY['dsn'],
            environment=settings.SENTRY.get('environment'),
            release=release,
        )
        logger.info("Sentry enabled.")

    def init_sentry(self, dsn, environment=None, release=None):
        """
        Sets up Sentry to send errors to the Sentry server.
        """
        sentry_sdk.init(
            dsn=dsn,
            integrations=[DjangoIntegration()],
            environment=environment,
            release=release,
        )

    def get_release(self):
        """Gets the "release" value. If one isn't given, it tries to get it
        from the project."""
        release = settings.SENTRY.get('release')
        if not release:
            release = get_from_repo()
        if not release and settings.SENTRY.get('git_sha_path'):
            release = get_from_file(settings.SENTRY.get('git_sha_path'))

        return release
