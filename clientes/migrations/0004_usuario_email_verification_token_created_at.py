"""
Migration: add email_verification_token_created_at to Usuario

Security fix 1.3: Email verification tokens previously had no expiry.
This field records when the token was issued so the view can reject
tokens older than 24 hours.
"""

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clientes", "0003_alter_usuario_foto"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="email_verification_token_created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                verbose_name="Token Criado em",
            ),
        ),
    ]
