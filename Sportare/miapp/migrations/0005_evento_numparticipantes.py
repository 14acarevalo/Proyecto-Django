# Generated by Django 5.1.3 on 2025-02-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0004_mensajes_alter_usuario_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='numParticipantes',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
