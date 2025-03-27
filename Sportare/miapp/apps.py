from django.apps import AppConfig


class MiappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'miapp'
    #Añadimos esto para cambiar el nombre de mi app a GestSport
    verbose_name = "Sportare"
    