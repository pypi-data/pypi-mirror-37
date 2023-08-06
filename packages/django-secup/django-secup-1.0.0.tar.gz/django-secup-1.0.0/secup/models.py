from django.db import models
from django.contrib.auth.models import User
from django.core.signing import dumps
from django.urls import reverse
from django.utils.http import urlquote
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from .settings import (SEND_SECUP_NOTIFICATION_MAILS, SUPERUSERS_AS_SECUP_MANAGERS, CUSTOM_SECUP_MANAGERS)
from .utils import file_name, secure_storage, send_notification


class SecureUpload(models.Model):
    uploader_email = models.EmailField(max_length=254, null=True, blank=True, verbose_name=_('Uploader Email'))
    uploader = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="uploader", verbose_name=_('Uploader'))
    receiver = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="receiver", verbose_name=_('Receiver'))
    file = models.FileField(upload_to=file_name, storage=secure_storage, null=True, blank=True, verbose_name=_('File'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __init__(self, *args, **kwargs):
        super(SecureUpload, self).__init__(*args, **kwargs)
        self._old_file = self.file

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Secure Uplaod')
        verbose_name_plural = _('Secure Uploads')

    def upload_url(self):
        """Creates signed upload url for invited person"""
        if not self.file:
            return reverse('secup:upload', args=[urlquote(dumps(self.id))])
        return None

    def files_url(self):
        """Auto login to django and view files with signed url"""
        if self.file and self.receiver and self.receiver.email:
            return reverse('secup:files_signed', args=[urlquote(dumps(self.receiver.email))])
        return None


@receiver(post_save, sender=SecureUpload)
def secup_notifications(sender, instance, created, **kwargs):
    if SEND_SECUP_NOTIFICATION_MAILS:
        template = None
        context = {'secure_upload': instance}
        if created:
            if instance.file:
                if not instance.receiver:
                    # New file uploaded to non exists staff user
                    if SUPERUSERS_AS_SECUP_MANAGERS:
                        to_list = User.objects.filter(email__isnull=False, is_active=True,
                                                      is_superuser=True).values_list('email', flat=True)
                    else:
                        to_list = [v for k, v in CUSTOM_SECUP_MANAGERS]
                    if len(to_list) > 0:
                        subject = _("New file uploaded for non exists staff user!")
                        template = 'email_managers'
                elif instance.receiver and instance.receiver.email:
                    # New file uploaded to staff user
                    to_list = [instance.receiver.email]
                    subject = _("New file uploaded to you!")
                    template = 'email_uploaded'
            else:
                if instance.uploader_email or (instance.uploader and instance.uploader.email):
                    # New invantation created
                    to_list = [instance.uploader.email]
                    subject = _("File upload request created for you!")
                    template = 'email_invited'
        else:
            if instance._old_file != instance.file and instance.receiver and instance.receiver.email:
                # New file uploaded from invantation
                to_list = [instance.receiver.email]
                subject = _("File uploaded from your invantation!")
                template = 'email_uploaded'
        if template:
            send_notification(subject, to_list, template, context)
