from django.conf import settings

if settings.APP_NAME == 'ambition_dashboard':
    from .tests import models
