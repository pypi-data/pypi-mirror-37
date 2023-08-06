from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.static import serve
from django.utils.http import urlunquote
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.core.signing import BadSignature, loads
from django.core.exceptions import SuspiciousOperation, MultipleObjectsReturned
from django.contrib.auth import login
from django.core.validators import EmailValidator
from .models import SecureUpload
from .forms import UploadFromInviteForm, UploadToSecupForm
from .settings import SUPERUSERS_AS_SECUP_MANAGERS, CUSTOM_SECUP_MANAGERS, SECUP_LINKS_VALID_SECONDS


def files(request, email=''):
    """
    Users have valid links can see files uploads created for them.
    """
    if not request.user.is_authenticated:
        try:
            email = loads(urlunquote(email), max_age=SECUP_LINKS_VALID_SECONDS)
        except BadSignature:
            raise SuspiciousOperation('Invalid URL or Link expired')
        try:
            user = get_object_or_404(User, email=email, is_active=True)
        except MultipleObjectsReturned:
            raise SuspiciousOperation('Multiple user exists with same email')
        login(request, user)
        request.user = user
    if not request.user.is_authenticated:
        raise Http404
    elif (
        (SUPERUSERS_AS_SECUP_MANAGERS and request.user.is_superuser) or
        (CUSTOM_SECUP_MANAGERS and request.user.email in [v for k, v in CUSTOM_SECUP_MANAGERS])
    ):
        uploads = SecureUpload.objects.all()
    else:
        uploads = SecureUpload.objects.filter(receiver=request.user)
    data = {
        'uploads': uploads
    }
    return render(request, 'secup/files.html', data)


@staff_member_required
def invite(request):
    """
    Staff can invite external users to upload file.
    """
    if request.method == "POST":
        email = request.POST.get('email', '')
        get_or_create_user = True if request.POST.get('get_or_create_user', 0) == 'True' else False
        validator = EmailValidator()
        validator(email)
        secure_upload = SecureUpload(receiver=request.user)
        if get_or_create_user:
            user, created = User.objects.get_or_create(username=email, email=email)
            secure_upload.uploader = user
        else:
            secure_upload.uploader_email = email
        secure_upload.save()
    return render(request, 'secup/invite.html', {})


def upload(request, signed_id):
    """
    Invited external users who have valid link, can upload file to secup.
    """
    try:
        secup = get_object_or_404(SecureUpload, file='', pk=loads(
            urlunquote(signed_id), max_age=SECUP_LINKS_VALID_SECONDS))
    except BadSignature:
        raise SuspiciousOperation('Invalid URL or File uploaded already or Link expired')
    form = UploadFromInviteForm(request.POST or None, request.FILES or None, instance=secup)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('secup:thanks')
    return render(request, 'secup/upload.html', {'form': form})


@login_required
def upload_to_secup(request):
    """
    Users can upload files to staff members. If user don't write a valid email, secup managers will notified.
    """
    form = UploadToSecupForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        secure_upload = form.save(commit=False)
        secure_upload.uploader = request.user
        secure_upload.save()
        return redirect('secup:thanks')
    return render(request, 'secup/upload_to_secup.html', {'form': form})


@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    """
    Serves secure files inside django app. Read warning!
    Only authorized secup managers can access all files, other users have to be reciver to access it.
    """
    if ((SUPERUSERS_AS_SECUP_MANAGERS and request.user.is_superuser) or
            (CUSTOM_SECUP_MANAGERS and request.user.email in [v for k, v in CUSTOM_SECUP_MANAGERS]) or
            (SecureUpload.objects.filter(file=path, receiver=request.user).exists())):
        return serve(request, path, document_root, show_indexes)
    raise Http404()
