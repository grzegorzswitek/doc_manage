# Generated by Django 3.2.3 on 2023-01-07 11:38

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import dokumentacja.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Branza",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nazwa", models.CharField(max_length=30)),
            ],
            options={
                "verbose_name": "Branża",
                "verbose_name_plural": "Branże",
            },
        ),
        migrations.CreateModel(
            name="Inwestycja",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nazwa", models.CharField(max_length=30)),
            ],
            options={
                "verbose_name": "Inwestycja",
                "verbose_name_plural": "Inwestycje",
            },
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nazwa", models.CharField(max_length=30)),
                ("opis", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Status",
                "verbose_name_plural": "Statusy",
            },
        ),
        migrations.CreateModel(
            name="Dokument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        storage=django.core.files.storage.FileSystemStorage(
                            base_url="/media/documents",
                            location="D:\\Users\\gswitek\\bx-panel-clear\\src\\panel\\media\\documents",
                        ),
                        upload_to="",
                    ),
                ),
                ("kod", models.CharField(editable=False, max_length=5, unique=True)),
                ("oznaczenie", models.CharField(max_length=50)),
                ("nazwa", models.CharField(max_length=200)),
                ("opis", models.TextField(blank=True)),
                ("komentarz", models.TextField(blank=True)),
                ("data_dokumentu", models.DateField()),
                ("data_dodania", models.DateField()),
                ("zarchiwizowany", models.BooleanField(default=False)),
                (
                    "branza",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="dokumentacja.branza",
                        verbose_name="Branża",
                    ),
                ),
                (
                    "dokument_nadrzedny",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="dokumentacja.dokument",
                        verbose_name="Dokument nadrzędny",
                    ),
                ),
                (
                    "inwestycja",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="dokumentacja.inwestycja",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="dokumentacja.status",
                    ),
                ),
            ],
            options={
                "verbose_name": "Dokument",
                "verbose_name_plural": "Dokumenty",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="adres e-mail"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(blank=True, max_length=30, verbose_name="imię"),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="nazwisko"
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="data dołączenia"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Aktywny"),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=True, verbose_name="W zespole"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Użytkownik",
                "verbose_name_plural": "Użytkownicy",
            },
            managers=[
                ("objects", dokumentacja.managers.CustomUserManager()),
            ],
        ),
    ]
