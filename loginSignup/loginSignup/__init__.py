"""
This module initializes the loginSignup app and sets up Celery tasks.
"""

from __future__ import absolute_import, unicode_literals

# Ensures app is imported at Django start so shared_task uses it.
from .celery import app as celery_app

__all__ = ("celery_app",)
