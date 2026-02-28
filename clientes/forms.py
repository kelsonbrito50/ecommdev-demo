"""Clientes app forms."""

from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Usuario


class RegistroForm(UserCreationForm):
    """User registration form."""

    class Meta:
        model = Usuario
        fields = ["email", "nome_completo", "telefone", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Email")}),
            "nome_completo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Nome Completo")}
            ),
            "telefone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Telefone")}
            ),
        }


class PerfilForm(forms.ModelForm):
    """User profile form."""

    class Meta:
        model = Usuario
        fields = [
            "nome_completo",
            "telefone",
            "cpf",
            "foto",
            "idioma_preferido",
            "notificacoes_email",
            "notificacoes_sms",
        ]
        widgets = {
            "nome_completo": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "foto": forms.FileInput(attrs={"class": "form-control"}),
            "idioma_preferido": forms.Select(attrs={"class": "form-control"}),
        }


class AlterarSenhaForm(PasswordChangeForm):
    """Change password form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
