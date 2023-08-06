from django.utils import timezone
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from smtplib import SMTPRecipientsRefused, SMTPDataError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .settings import SECURE_MEDIA_URL_PREFIX, SECURE_MEDIA_ROOT


def send_notification(subject, to_list, template, context):
    text_content = render_to_string('secup/{}.txt'.format(template), context)
    html_content = render_to_string('secup/{}.html'.format(template), context)
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, to_list)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except (SMTPRecipientsRefused, SMTPDataError):
        pass


def file_name(instance, filename):
    """
    Generate slugified file names inside folders such as: /Year/Month/SlugifyiedFilename[.extention]
    """
    now = timezone.now()
    extention = filename.split('.')[-1].strip().lower() if '.' in filename else 'none'
    name = "".join(filename.split('.')[:-1]).strip().lower() if '.' in filename else 'Untitled'
    return '{}/{}/{}.{}'.format(
        now.strftime("%Y"), now.strftime("%m"), slugify(name)[:150], extention
    )


secure_storage = FileSystemStorage(location=SECURE_MEDIA_ROOT, base_url='/secup/{}'.format(SECURE_MEDIA_URL_PREFIX))
