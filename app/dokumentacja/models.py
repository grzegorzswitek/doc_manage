from os import path
from django.contrib.auth.decorators import login_required

from django.db import models
from django.db.models.fields import BooleanField
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

from panel.settings import MEDIA_ROOT, MEDIA_URL
from dokumentacja.managers import DokumentCurrentManager

DOKUMENT_FILE_STORAGE = FileSystemStorage(
    location=path.join(MEDIA_ROOT, "documents"),
    base_url=path.join(MEDIA_URL, "documents"),
)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Inwestycja(models.Model):
    nazwa = models.CharField(max_length=30)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Inwestycja"
        verbose_name_plural = "Inwestycje"

    def natural_key(self):
        return self.nazwa

    def get_absolute_url(self):
        return reverse("dokumentacja:inwestycja_detail", args=[str(self.id)])


class Branza(models.Model):
    nazwa = models.CharField(max_length=30)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Branża"
        verbose_name_plural = "Branże"

    def natural_key(self):
        return self.nazwa


class Status(models.Model):
    nazwa = models.CharField(max_length=30)
    opis = models.TextField(blank=True)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statusy"

    def natural_key(self):
        return self.nazwa


class Dokument(models.Model):
    file = models.FileField(storage=DOKUMENT_FILE_STORAGE)
    kod = models.CharField(max_length=5, unique=True, editable=False)
    inwestycja = models.ForeignKey(Inwestycja, on_delete=models.SET_NULL, null=True)
    branza = models.ForeignKey(
        Branza, verbose_name="Branża", on_delete=models.SET_NULL, null=True
    )
    oznaczenie = models.CharField(max_length=50)
    nazwa = models.CharField(max_length=200)
    opis = models.TextField(blank=True)
    komentarz = models.TextField(blank=True)
    data_dokumentu = models.DateField()
    data_dodania = models.DateField()
    dokument_nadrzedny = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Dokument nadrzędny",
    )
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    zarchiwizowany = models.BooleanField(default=False)

    objects = models.Manager()
    objects_current = DokumentCurrentManager()

    @property
    def dokumenty_podrzedne(self):
        dokumenty_qs = Dokument.objects.filter(dokument_nadrzedny=self)
        return dokumenty_qs

    @property
    def url_change(self):
        return reverse("dokumentacja:edytuj_dokument", args=[str(self.pk)])

    def __str__(self):
        return self.nazwa + " (" + self.oznaczenie + ")"

    class Meta:
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumenty"

    def natural_key(self):
        return self.nazwa

    def get_absolute_url(self):
        return reverse("dokumentacja:dokument_detail", args=[str(self.pk)])
