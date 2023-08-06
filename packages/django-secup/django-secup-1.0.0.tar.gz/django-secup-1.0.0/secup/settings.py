import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


SUPERUSERS_AS_SECUP_MANAGERS = getattr(settings, 'SUPERUSERS_AS_SECUP_MANAGERS', False)
CUSTOM_SECUP_MANAGERS = getattr(settings, 'CUSTOM_SECUP_MANAGERS', None)
if not SUPERUSERS_AS_SECUP_MANAGERS and not CUSTOM_SECUP_MANAGERS:
    raise ImproperlyConfigured('You must either define SUPERUSERS_AS_SECUP_MANAGERS as True\
 or define CUSTOM_SECUP_MANAGERS in the settings!')

prefix = getattr(settings, 'SECURE_MEDIA_URL_PREFIX', '/secure-media/')
SECURE_MEDIA_URL_PREFIX = prefix[1:] if prefix[:1] == '/' else prefix
SECURE_MEDIA_ROOT = getattr(settings, 'SECURE_MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'secure-media/'))

SEND_SECUP_NOTIFICATION_MAILS = getattr(settings, 'SEND_SECUP_NOTIFICATION_MAILS', False)
SECUP_LINKS_VALID_SECONDS = getattr(settings, 'SECUP_LINKS_VALID_SECONDS', 7200)
try:
    SECUP_LINKS_VALID_SECONDS = int(SECUP_LINKS_VALID_SECONDS)
except ValueError:
    raise ImproperlyConfigured('SECUP_LINKS_VALID_SECONDS should be an intiger value!')
