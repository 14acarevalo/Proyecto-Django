from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager #Para personalizar el usuario
# Create your models here.

#Llevamos a cabo la creacion de usuarios flexibles
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Encriptamos la contraseña de manera segura
        user.save(using=self._db)
        return user

    #Vamos a encriptar la contraseña con este metodo
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_coordinador', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    password = models.CharField(max_length=128)  # Campo para contraseña cifrada
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    is_coordinador = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Configura email como el identificador único
    REQUIRED_FIELDS = ['nombre', 'apellidos']  # Campos obligatorios para crear usuarios
    
    objects = UsuarioManager()  # Manager personalizado
    
    imagen = models.ImageField(upload_to='usuarios/', null=True, blank=True)


    def __str__(self):
        return f"Nombre: {self.nombre} - Apellidos: {self.apellidos}  - Dni: {self.dni} - Tlf: {self.telefono} - Correo electronico: {self.email} "
    

class Evento(models.Model):
    CATEGORIA_CHOICES = [
        ('deportivo', 'Deportivo'),
        ('cultural', 'Cultural'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    fechaRealizacion = models.DateField(null=True, blank=True)
    fechaInscripcion = models.DateField()
    fechaCierre = models.DateField()
    hora = models.TimeField(verbose_name="Hora de realización")
    precio = models.IntegerField()
    numParticipantes = models.IntegerField()
    usuarios = models.ManyToManyField('Usuario')
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES, default='deportivo')

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()}) - {self.fechaRealizacion}"

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"


class Pago(models.Model):
    cantidad = models.IntegerField()  # Cantidad del pago (el precio de la actividad)
    fechaPago = models.DateField()  # Fecha en que se realizó el pago
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)  # Usuario que realizó el pago
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE)  # Evento para el que se ha hecho el pago

    def __str__(self):
        return f"Pago de {self.cantidad} realizado el {self.fechaPago} por {self.usuario}"


class Mensajes(models.Model):
    nombre = models.CharField(max_length=200)  # Nombre del usuario
    email = models.EmailField()               # Campo específico para correos electrónicos, por eso pongo emailField
    texto = models.TextField()                # Campo más adecuado para textos largos, ya que dependerá de la sugerencia del usuario

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.email})"
    
