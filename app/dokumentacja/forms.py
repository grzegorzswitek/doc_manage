from django import forms
from django.forms import fields

from .models import Dokument, Inwestycja


class DodajDokumentForm(forms.ModelForm):
    class Meta:
        model = Dokument
        fields = "__all__"
        exclude = [
            "status",
            "zarchiwizowany",
        ]


class EdytujDokumentForm(forms.ModelForm):
    class Meta:
        model = Dokument
        fields = "__all__"
        exclude = [
            "file",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "instance" in kwargs:
            instance = kwargs["instance"]
            inwestycja = instance.inwestycja
            branza = instance.branza
            dokumenty_nadrzedne = Dokument.objects.filter(
                inwestycja=inwestycja, branza=branza
            )
            self.fields["dokument_nadrzedny"] = forms.ModelChoiceField(
                queryset=dokumenty_nadrzedne, required=False
            )
