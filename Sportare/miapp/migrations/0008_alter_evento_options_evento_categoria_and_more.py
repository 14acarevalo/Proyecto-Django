# Generated by Django 5.1.3 on 2025-03-08 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0007_usuario_imagen'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evento',
            options={'verbose_name': 'Evento', 'verbose_name_plural': 'Eventos'},
        ),
        migrations.AddField(
            model_name='evento',
            name='categoria',
            field=models.CharField(choices=[('deportivo', 'Deportivo'), ('cultural', 'Cultural')], default='deportivo', max_length=10),
        ),
        migrations.AlterField(
            model_name='evento',
            name='hora',
            field=models.TimeField(verbose_name='Hora de realización'),
        ),
    ]
