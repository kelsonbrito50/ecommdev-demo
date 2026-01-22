"""Clientes app URLs."""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'clientes'

urlpatterns = [
    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.RegistroView.as_view(), name='registro'),

    # Email verification
    path('verificar-email/<uuid:token>/', views.VerificarEmailView.as_view(), name='verificar_email'),
    path('verificar-email/enviado/', views.VerificarEmailEnviadoView.as_view(), name='verificar_email_enviado'),
    path('verificar-email/reenviar/', views.ReenviarVerificacaoView.as_view(), name='reenviar_verificacao'),

    # Password reset
    path('senha/reset/', auth_views.PasswordResetView.as_view(
        template_name='clientes/password_reset.html'
    ), name='password_reset'),
    path('senha/reset/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='clientes/password_reset_done.html'
    ), name='password_reset_done'),
    path('senha/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='clientes/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('senha/reset/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='clientes/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Profile
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', views.PerfilEditarView.as_view(), name='perfil_editar'),
    path('perfil/senha/', views.AlterarSenhaView.as_view(), name='alterar_senha'),
    path('perfil/sessoes/', views.SessoesView.as_view(), name='sessoes'),
]
