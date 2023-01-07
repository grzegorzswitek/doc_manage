from django.urls import path
from django.conf.urls.static import static

from .views import (
    DokumentDetailView,
    DodajDokument,
    DodajDokumentSeriall,
    dokumenty_branzy_inwestycji,
    SprawdzDokument,
    ajax_get_document_by_code,
    ajax_search_qrcode_by_image,
    WykazDokumentow,
    EdytujDokument,
    ZastapDokument,
    DokumentUpdateActionView,
    PobierzDokumentyView,
)

app_name = "dokumentacja"

urlpatterns = [
    # Dodaj dokument
    path("dodaj", DodajDokument.as_view(), name="dodaj_dokument"),
    path(
        "dodaj-dokumenty-seriall",
        DodajDokumentSeriall.as_view(),
        name="dodaj_dokumenty_seriall",
    ),
    path(
        "ajax/rysunki-branzy-inwestycji",
        dokumenty_branzy_inwestycji,
        name="ajax_dokumenty_branzy_inwestycji",
    ),
    # Sprawdź dokument
    path("sprawdz", SprawdzDokument.as_view(), name="sprawdz_dokument"),
    path(
        "ajax/get-document-by-code",
        ajax_get_document_by_code,
        name="ajax_get_document_by_code",
    ),
    path(
        "ajax/ajax-search-qrcode-by-image",
        ajax_search_qrcode_by_image,
        name="ajax_search_qrcode_by_image",
    ),
    # Wykaz dokumentów
    path("wykaz", WykazDokumentow.as_view(), name="wykaz_dokumentow"),
    # Dokument Detail
    path("dokument/<int:pk>", DokumentDetailView.as_view(), name="dokument_detail"),
    # Edytuj dokument
    path("dokument/<int:pk>/edytuj", EdytujDokument.as_view(), name="edytuj_dokument"),
    # Zastąp dokument
    path("dokument/<int:pk>/zastap", ZastapDokument.as_view(), name="zastap_dokument"),
    # Dokument akcje
    path("dokument/action", DokumentUpdateActionView.as_view(), name="dokument_action"),
]
