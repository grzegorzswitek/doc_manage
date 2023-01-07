from datetime import date
import json
from random import choice
import string
from os import path
import sys
import re

from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.http.response import Http404
from urllib.parse import urlencode
from django.shortcuts import render, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Inwestycja,
    Branza,
    Dokument,
    Status,
    User,
)
from .models import DOKUMENT_FILE_STORAGE
from .forms import (
    DodajDokumentForm,
    EdytujDokumentForm,
)
from .src import add_qrcode_to_pdf
from .extension import Plural


class DodajDokument(View):
    form_class = DodajDokumentForm
    template_name = "dokumentacja/dodaj-dokument.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("dokumentacja.add_dokument"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def _generuj_kod(self):
        kod = ""
        while True:
            kod = "".join(
                choice(string.ascii_letters + string.digits) for i in range(5)
            )
            queryset = Dokument.objects.filter(kod=kod)
            if not bool(queryset):
                break
        return kod

    def get(self, request, *args, **kwargs):
        initial = request.GET.dict()
        initial.update({"data_dodania": date.today().isoformat()})
        form = self.form_class(initial=initial)
        print(initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        kod = self._generuj_kod()
        form = self.form_class(request.POST, request.FILES)
        form.fields["data_dodania"].value = date.today().isoformat()
        filename = request.FILES.get("file").name
        if form.is_valid():
            dokument = form.save(commit=False)
            dokument.kod = kod
            dokument.data_dodania = date.today().isoformat()
            AKTUALNY = Status.objects.get(nazwa="Aktualny")
            dokument.status = AKTUALNY
            dokument.save()

            dokument_path = path.join(
                DOKUMENT_FILE_STORAGE.location, dokument.file.path
            )
            qr_x = request.POST.get("qr_x")
            qr_y = request.POST.get("qr_y")
            add_qrcode_to_pdf.PdfDoc(
                path=dokument_path, qr_code=dokument.kod, qr_coords=(qr_x, qr_y)
            )

            dokument.save()
            return FileResponse(dokument.file, as_attachment=True, filename=filename)
        print(form.errors)
        print(form.fields)
        return render(request, self.template_name, {"form": form})


class DodajDokumentSeriall(View):
    form_class = DodajDokumentForm
    template_name = "dokumentacja/dodaj-dokument.html"

    def _generuj_kod(self):
        kod = ""
        while True:
            kod = "".join(
                choice(string.ascii_letters + string.digits) for i in range(5)
            )
            queryset = Dokument.objects.filter(kod=kod)
            if not bool(queryset):
                break
        return kod

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        kod = self._generuj_kod()
        post_data = request.POST.dict()
        post_data["inwestycja"] = Inwestycja.objects.get(nazwa=post_data["inwestycja"])
        post_data["branza"] = Branza.objects.get(nazwa=post_data["branza"])
        form = self.form_class(post_data, request.FILES)
        filename = request.FILES.get("file").name
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            dokument = form.save(commit=False)
            dokument.kod = kod
            dokument.data_dodania = date.today().isoformat()
            AKTUALNY = Status.objects.get(nazwa="Aktualny")
            dokument.status = AKTUALNY
            dokument.save()

            dokument_path = path.join(
                DOKUMENT_FILE_STORAGE.location, dokument.file.path
            )
            qr_x = request.POST.get("qr_x")
            qr_y = request.POST.get("qr_y")
            add_qrcode_to_pdf.PdfDoc(
                path=dokument_path, qr_code=dokument.kod, qr_coords=(qr_x, qr_y)
            )

            dokument.save()
            return FileResponse(dokument.file, as_attachment=True, filename=filename)
        return render(request, self.template_name, {"form": form})


class ZastapDokument(View):

    template_name = "dokumentacja/zastap-dokument.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("dokumentacja.change_dokument"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        try:
            dokument = Dokument.objects.get(pk=pk)
        except:
            return render(
                request,
                template_name=self.template_name,
                context={"errors": ["Nie znaleziono dokumentu"]},
            )

        try:
            STATUS_NIEAKTUALNY = Status.objects.get(nazwa="Nieaktualny")
        except:
            return render(
                request,
                template_name=self.template_name,
                context={"errors": ['Nie znaleziono statusu "Nieaktualny"']},
            )

        dokument.status = STATUS_NIEAKTUALNY

        try:
            dokument.save()
        except Exception as e:
            return render(
                request, template_name=self.template_name, context={"errors": [str(e)]}
            )

        base_url = reverse("dokumentacja:dodaj_dokument")
        query_string = urlencode(
            {
                "inwestycja": dokument.inwestycja.pk,
                "branza": dokument.branza.pk,
                "oznaczenie": dokument.oznaczenie,
                "nazwa": dokument.nazwa,
            }
        )

        url = "{}?{}".format(base_url, query_string)
        return HttpResponseRedirect(url)


class EdytujDokument(View):

    form_class = EdytujDokumentForm
    template_name = "dokumentacja/edytuj-dokument.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("dokumentacja.change_dokument"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        dokument = Dokument.objects.get(pk=pk)
        form = self.form_class(instance=dokument)
        return render(request, template_name=self.template_name, context={"form": form})

    def post(self, request, pk, *args, **kwargs):
        dokument = dokument = Dokument.objects.get(pk=pk)
        form = self.form_class(request.POST, instance=dokument)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("dokumentacja:dokument_detail", args=(pk,))
            )
        return render(request, template_name=self.template_name, context={"form": form})


def dokumenty_branzy_inwestycji(request):
    if request.is_ajax and request.method == "POST":
        pk_inwestycja = request.POST.dict()["pk_inwestycja"]
        pk_branza = request.POST.dict()["pk_branza"]
        dokumenty_nadrzedne = Dokument.objects.filter(inwestycja=pk_inwestycja).filter(
            branza=pk_branza
        )
        ser_dokumenty_nadrzedne = serializers.serialize("json", dokumenty_nadrzedne)
        return JsonResponse(
            {"dokumenty_nadrzedne": ser_dokumenty_nadrzedne}, status=200
        )


class DokumentDetailView(DetailView):
    model = Dokument
    template_name = "dokumentacja/dokument_detail.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("dokumentacja.view_dokument"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SprawdzDokument(View):
    template_name = "dokumentacja/sprawdz-dokument.html"

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={})


def ajax_get_document_by_code(request):
    if request.is_ajax and request.method == "GET":
        kod = request.GET.get("kod")
        try:
            dokument = Dokument.objects.get(kod=kod)
        except Exception as e:
            return JsonResponse({"error": "Nie znaleziono dokumentu"}, status=200)

        ser_data = {
            "dokument": serializers.serialize(
                "json", [dokument], use_natural_foreign_keys=True
            )
        }
        dokument_nadrzedny = dokument.dokument_nadrzedny
        if dokument_nadrzedny:
            ser_data.update(
                {
                    "dokument_nadrzedny": serializers.serialize(
                        "json",
                        [dokument_nadrzedny],
                    )
                }
            )
        else:
            ser_data.update({"dokument_nadrzedny": None})

        dokumenty_podrzedne = Dokument.objects.filter(dokument_nadrzedny=dokument.pk)
        if dokumenty_podrzedne:
            ser_data.update(
                {
                    "dokumenty_podrzedne": serializers.serialize(
                        "json", dokumenty_podrzedne
                    )
                }
            )
        else:
            ser_data.update({"dokumenty_podrzedne": None})

        ser_data.update({"url_change": json.dumps([dokument.url_change])})
        ser_data.update({"url_detail": json.dumps([dokument.get_absolute_url()])})

        return JsonResponse(ser_data, status=200)


def ajax_search_qrcode_by_image(request):
    file = request.FILES.get("file")

    from pyzbar.pyzbar import decode
    from PIL import Image
    import fitz

    doc = fitz.open(stream=file.read(), filetype="pdf")
    page = doc.loadPage(0)
    pix = page.getPixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    qr_decode = decode(img)
    if len(qr_decode):
        data = qr_decode[0].data.decode()
        return JsonResponse({"kod": data}, status=200)
    return JsonResponse({"error": "Nie znaleziono kodu w pliku pdf"}, status=200)


class WykazDokumentow(View):
    template_name = "dokumentacja/wykaz-dokumentow.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("dokumentacja.view_dokument"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    class FilterPkOrNazwa:
        def __init__(self, filter_values, model, *args, **kwargs):
            if type(filter_values) is str:
                self.filter_values = [
                    val.strip() for val in filter_values.split(",") if bool(val)
                ]
            elif type(filter_values) is list:
                self.filter_values = filter_values
            else:
                raise TypeError("Must be list or str")
            self.model = model

        def _get_pk_and_name_filter(self):
            filter_dict = {"pk": [], "nazwa": []}
            for val in self.filter_values:
                try:
                    val = int(val)
                    filter_dict["pk"].append(val)
                except ValueError:
                    filter_dict["nazwa"].append(val)
                except:
                    print(sys.exc_info()[0])

            return filter_dict

        @property
        def objects(self):
            queryset = self.model.objects.none()
            queryset |= self.model.objects.filter(
                pk__in=self._get_pk_and_name_filter()["pk"]
            )
            queryset |= self.model.objects.filter(
                nazwa__in=self._get_pk_and_name_filter()["nazwa"]
            )
            return queryset

    class FilterDate:
        def __init__(self, date_str: str, field: str):
            self.date_str = date_str
            self.field = field

        def _parse_string(self):
            from datetime import date, timedelta

            patt_gte = "^>(\d{8})$"
            patt_lte = "^<(\d{8})$"
            patt_btw = "^(\d{8})-(\d{8})$"
            patt_eq = "^(\d{8})$"
            result = re.match(patt_gte, self.date_str)
            if result is not None:
                (date_combined,) = result.groups()
                year = int(date_combined[:4])
                month = int(date_combined[4:6])
                day = int(date_combined[6:])
                return {f"{self.field}__gte": date(year, month, day)}
            result = re.match(patt_lte, self.date_str)
            if result is not None:
                (date_combined,) = result.groups()
                year = int(date_combined[:4])
                month = int(date_combined[4:6])
                day = int(date_combined[6:])
                return {f"{self.field}__lte": date(year, month, day)}
            result = re.match(patt_eq, self.date_str)
            if result is not None:
                (date_combined,) = result.groups()
                year = int(date_combined[:4])
                month = int(date_combined[4:6])
                day = int(date_combined[6:])
                return {f"{self.field}": date(year, month, day)}
            result = re.match(patt_btw, self.date_str)
            if result is not None:
                date_combined_gte, date_combined_lte = result.groups()
                date_gte = date(
                    year=int(date_combined_gte[:4]),
                    month=int(date_combined_gte[4:6]),
                    day=int(date_combined_gte[6:]),
                )
                date_lte = date(
                    year=int(date_combined_lte[:4]),
                    month=int(date_combined_lte[4:6]),
                    day=int(date_combined_lte[6:]),
                )
                return {f"{self.field}__gte": date_gte, f"{self.field}__lte": date_lte}
            return {}

        def __iter__(self):
            for key, value in self._parse_string().items():
                yield key, value

    def get(self, request, *args, **kwargs):

        user = request.user

        nieaktualne = (
            True
            if request.GET.get("nieaktualne", False) in ("1", "true", "True")
            else False
        )
        zarchiwizowane = (
            True
            if request.GET.get("zarchiwizowane", False) in ("1", "true", "True")
            else False
        )

        filters = {}
        get_inwestycja = request.GET.get("inwestycja", False)
        if get_inwestycja:
            filters["inwestycja__in"] = self.FilterPkOrNazwa(
                get_inwestycja, Inwestycja
            ).objects
        get_branza = request.GET.get("branza", False)
        if get_branza:
            filters["branza__in"] = self.FilterPkOrNazwa(get_branza, Branza).objects
        get_status = request.GET.get("status", False)
        if get_status:
            filters["status__in"] = self.FilterPkOrNazwa(get_status, Status).objects

        get_data_dodania = request.GET.get("data_dodania", False)
        if get_data_dodania:
            fil = self.FilterDate(get_data_dodania, "data_dodania")
            filters.update(**dict(fil))
        get_data_dokumentu = request.GET.get("data_dokumentu", False)
        if get_data_dokumentu:
            fil = self.FilterDate(get_data_dokumentu, "data_dokumentu")
            filters.update(**dict(fil))

        if not (nieaktualne or zarchiwizowane):
            queryset = Dokument.objects_current.all()
        else:
            queryset = Dokument.objects.all()
            if not zarchiwizowane:
                queryset = queryset.filter(zarchiwizowany=False)
            if not nieaktualne:
                status_nieaktualny = Status.objects.get(nazwa="Nieaktualny")
                queryset = queryset.exclude(status=status_nieaktualny)

        inwestycje = list(set([dokument.inwestycja for dokument in queryset]))
        branze = list(set([dokument.branza for dokument in queryset]))
        statusy = list(set([dokument.status for dokument in queryset]))
        daty_dodania = list(set([dokument.data_dodania for dokument in queryset])) or (
            date(2000, 1, 1),
            date.today(),
        )
        daty_dokumentu = list(
            set([dokument.data_dokumentu for dokument in queryset])
        ) or (date(2000, 1, 1), date.today())
        filter_table = {
            "inwestycja": inwestycje,
            "branza": branze,
            "status": statusy,
            "data_dodania": (min(daty_dodania), max(daty_dodania)),
            "data_dokumentu": (min(daty_dokumentu), max(daty_dokumentu)),
        }

        filters_user = {**filters}
        filters_user["zarchiwizowane"] = request.GET.get("zarchiwizowane", False)
        filters_user["nieaktualne"] = request.GET.get("nieaktualne", False)
        filters_user["data_dodania"] = {
            "od": filters.get("data_dodania__gte", filter_table["data_dodania"][0]),
            "do": filters.get("data_dodania__lte", filter_table["data_dodania"][1]),
            "min": filter_table["data_dodania"][0],
            "max": filter_table["data_dodania"][1],
        }
        filters_user["data_dokumentu"] = {
            "od": filters.get("data_dokumentu__gte", filter_table["data_dokumentu"][0]),
            "do": filters.get("data_dokumentu__lte", filter_table["data_dokumentu"][1]),
            "min": filter_table["data_dokumentu"][0],
            "max": filter_table["data_dokumentu"][1],
        }

        queryset = queryset.filter(**filters)

        # Akcje (np. Status → Nieaktualny)

        statusy = Status.objects.all()

        return render(
            request,
            template_name=self.template_name,
            context={
                "dokumenty": queryset,
                "filter_table": filter_table,
                "filters_user": filters_user,
                "statusy": statusy,
            },
        )


class DokumentUpdateActionView(View):
    template_name = "dokumentacja/dokument-akcje.html"

    @method_decorator(login_required)
    @method_decorator(permission_required("dokumentacja.view_dokument"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def _get_documents(self, pk):
        if not bool(pk):
            raise Exception("Należy podać listę pk Dokumentów")
        try:
            pk = pk.split(",")
            dokumenty = Dokument.objects.filter(pk__in=pk)
        except ValueError:
            raise Exception(
                "Niepoprawne wartości pk Dokumentów, oczekiwane wartości liczbowe"
            )
        if not dokumenty.count():
            raise Exception("Nie znaleziono Dokumentów o podanych kluczach")
        return dokumenty

    def _change_status(self, dokumenty, status):
        try:
            status = Status.objects.get(pk=status)
        except ObjectDoesNotExist:
            raise Exception("Status nie istnieje")
        except Exception as e:
            raise Exception(e)

        for dokument in dokumenty:
            dokument.status = status

        try:
            Dokument.objects.bulk_update(dokumenty, ["status"])
            ile_dokumentow = len(dokumenty)
            return f"Pomyślnie zaktualizowano {Plural(ile_dokumentow, 'dokument', 'dokumenty', 'dokumentów')}"
        except Exception as e:
            raise Exception(f'Błąd: "{str(e)}"')

    def _change_zarchiwizowany(self, dokumenty, zarchiwizowany):
        if zarchiwizowany is None or zarchiwizowany not in ("0", "1"):
            raise Exception('Niepoprawna wartość "zarchiwizowany". Oczekiwane 0 lub 1.')

        for dokument in dokumenty:
            dokument.zarchiwizowany = bool(int(zarchiwizowany))

        try:
            Dokument.objects.bulk_update(dokumenty, ["zarchiwizowany"])
            ile_dokumentow = len(dokumenty)
            return f"Pomyślnie zaktualizowano {Plural(ile_dokumentow, 'dokument', 'dokumenty', 'dokumentów')}"
        except Exception as e:
            raise Exception(f'Błąd: "{str(e)}"')

    def _download_files(self, dokumenty):
        from django.http import StreamingHttpResponse
        import zipstream

        def _filepath_arc(dokument, inwestycje=True, branze=True, nieaktualny=False):
            filepath = dokument.file.path
            _, ext = path.splitext(filepath)
            if nieaktualny:
                filename = (
                    f"{dokument.oznaczenie} -- {dokument.nazwa} (nieaktualny){ext}"
                )
            else:
                filename = f"{dokument.oznaczenie} -- {(dokument.nazwa)}{ext}"
            if inwestycje:
                return (filepath, f"{dokument.inwestycja}/{dokument.branza}/{filename}")
            if branze:
                return (filepath, f"{dokument.branza}/{filename}")
            return (filepath, filename)

        dir_inwestycje = False
        dir_branze = False
        inwestycje = list(set([dokument.inwestycja for dokument in dokumenty]))
        if len(inwestycje) > 1:
            dir_inwestycje = True
        else:
            branze = list(set([dokument.branza for dokument in dokumenty]))
            if len(branze) > 1:
                dir_branze = True

        try:
            STATUS_NIEAKTUALNY = Status.objects.filter(nazwa="Nieaktualny")[0]
        except:
            STATUS_NIEAKTUALNY = None

        z = zipstream.ZipFile(mode="w", compression=zipstream.ZIP_DEFLATED)
        for dokument in dokumenty:
            nieaktualny = True if dokument.status == STATUS_NIEAKTUALNY else False
            z.write(
                *_filepath_arc(
                    dokument,
                    inwestycje=dir_inwestycje,
                    branze=dir_branze,
                    nieaktualny=nieaktualny,
                )
            )

        response = StreamingHttpResponse(z, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename={}".format("files.zip")
        return response

    def post(self, request, *args, **kwargs):
        pk = request.POST.get("pk", None)
        action = request.POST.get("action", None)

        if action is None:
            return JsonResponse({"errors": ["Nie podano akcji"]})

        try:
            dokumenty = self._get_documents(pk)
        except Exception as e:
            return JsonResponse({"errors": [str(e)]}, status=200)

        if action == "update_status":
            status = request.POST.get("value", None)

            try:
                info = self._change_status(dokumenty, status)
                return JsonResponse({"success": True, "info": info}, status=200)
            except Exception as e:
                return JsonResponse({"errors": [str(e)]}, status=200)

        if action == "update_zarchiwizowany":
            zarchiwizowany = request.POST.get("value", None)

            try:
                info = self._change_zarchiwizowany(dokumenty, zarchiwizowany)
                return JsonResponse({"success": True, "info": info})
            except Exception as e:
                return JsonResponse({"errors": [str(e)]})

        if action == "download_files":
            try:
                return self._download_files(dokumenty)
            except Exception as e:
                return JsonResponse({"errors": [str(e)]})

        if action == "download_files_link":
            pass


class PobierzDokumentyView(View):

    template_name = "dokumentacja/pobierz-dokumenty.html"

    def get(self, request, *args, **kwargs):
        download = request.GET.get("download", None)
        link = kwargs.get("link", None)

        return render(request, template_name=self.template_name)
