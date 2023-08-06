from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, EmailField, TextInput
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import SecureUpload


class UploadFromInviteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = True

    class Meta:
        model = SecureUpload
        fields = ('file', 'description')


class UploadToSecupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = True

    receiver_mail = EmailField(
        required=False,
        label=_('Staff member email'),
        widget=TextInput(attrs={'size': 40}),
    )

    class Meta:
        model = SecureUpload
        fields = ('file', 'description', 'receiver_mail')

    def save(self, commit=True):
        obj = super().save(commit=False)
        receiver_mail = self.cleaned_data['receiver_mail']
        try:
            self.instance.receiver = User.objects.get(email=receiver_mail, is_staff=True, is_active=True)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass
        obj.save()
        return obj
