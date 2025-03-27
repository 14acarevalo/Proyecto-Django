from django.shortcuts import render, redirect, HttpResponse
from .models import Evento, Usuario  # Importación correcta del modelo
from datetime import datetime
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages #Este libreria me va ayudar flask
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #Este me va ayudar para ocultar información a usuarios no logeados
from .forms import MensajesForm, UsuarioForm
from django.shortcuts import get_object_or_404
from .models import Mensajes  # Asegúrate de importar el modelo correcto
from django.apps import apps
from django.conf import settings
from django.utils.timezone import localdate
from django.utils.timezone import now
from .models import Pago  # 👈 Asegúrate de importar Pago





#Paginas complementarias

def inicio(request):
    return render(request, 'miapp/inicio.html')

def contacto(request):
    if request.method == "POST":
        form = MensajesForm(request.POST)
        print("Datos recibidos:", request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mensaje enviado correctamente!")
            return redirect('contacto')
        else:
            messages.error(request, "Hubo un error al enviar el mensaje.")
            return render(request, 'miapp/contacto.html', {'form': form})
    else:
        form = MensajesForm()
        return render(request, 'miapp/contacto.html', {'form': form})

def servicio(request):
    return render (request, 'miapp/servicio.html' )
def menuUsuariosCoordinador(request):
    return render(request, 'miapp/menuUsuariosCoordinador.html')

#Páginas menu actividades culturales
def menuActividadesCoordinador(request):
    evento = Evento.objects.first()  
    
    if evento.categoria == 'deportivo':
        return render(request, 'miapp/menuActividadesDeportivasCoordinador.html')

#Páginas menu actividades culturales

def menuActividadesCulturalesCoordinador(request):
    # Obtenemos todos los eventos de categoría cultural
    eventos_culturales = Evento.objects.filter(categoria='cultural')

    if not eventos_culturales.exists():  # Si no hay eventos culturales
        return HttpResponse("No hay eventos culturales disponibles.", status=404)

    # Si hay eventos culturales, los pasamos al template
    return render(request, 'miapp/menuActividadesCulturalesCoordinador.html', {'eventos': eventos_culturales})



def nosotros(request):
    return render (request, 'miapp/nosotros.html' )

def menu(request):
    return render (request, 'miapp/menu.html')

#Metodo para acceder y para cerrar sesión

def login_page(request):
    if request.method == 'POST':
        print(request.POST)

        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")  # Para depuración

        try:
            # Obtener el usuario por el email
            user = Usuario.objects.get(email=email)
            
            # Verificar si la contraseña coincide
            if check_password(password, user.password):
                login(request, user)
                return render(request, 'miapp/menu.html')  # Cambia por la URL adecuada
            else:
                messages.warning(request, 'Credenciales incorrectas')
        except Usuario.DoesNotExist:
            messages.warning(request, 'Usuario no encontrado')
            
    return render(request, 'miapp/login.html')

def logout_out(request):
    logout(request)
    return render (request, "miapp/login.html")

#Métodos del usuario

def register_user(request):
    register_form = RegisterForm()
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
    
    return render(request, 'miapp/register.html', {
        'nombre': 'Registro',
        'register_form': register_form
    })

#A través de este metodo creamos el usuario, cuando se insertan en nuestra base de datos

def crear_usuario(request):
    if request.method == 'POST':
        try:
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            dni = request.POST['dni']
            telefono = request.POST['telefono']
            email = request.POST['email']
            direccion = request.POST['direccion']
            ciudad = request.POST['ciudad']
            password = request.POST.get('password', 'default_password')

            # Obtener la imagen del formulario
            imagen = request.FILES.get('imagen')  # Usamos request.FILES para obtener la imagen

            # Verificar si el email o el DNI ya existen en la base de datos
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
                return render(request, 'miapp/insertarUsuario.html')

            if Usuario.objects.filter(dni=dni).exists():
                messages.error(request, 'Ya existe un usuario con ese DNI.')
                return render(request, 'miapp/insertarUsuario.html')

            # Verificar si la casilla de "coordinador" está marcada
            is_coordinador = 'is_coordinador' in request.POST

            # Crear y guardar el usuario con la contraseña encriptada
            usuario = Usuario(
                nombre=nombre,
                apellidos=apellidos,
                dni=dni,
                telefono=telefono,
                email=email,
                direccion=direccion,
                ciudad=ciudad,
                password=make_password(password),
                is_coordinador=is_coordinador,
                imagen=imagen  # Guardamos la imagen
            )
            usuario.save()
            messages.success(request, f'Usuario creado correctamente con nombre: {usuario.nombre}')
            return redirect('login')

        # Mandar mensaje en el registro por si acaso algún dato único ya está siendo utilizado
        except IntegrityError:
            messages.error(request, "Error: Ya existe un usuario con ese email o DNI.")
            return render(request, 'miapp/insertarUsuario.html')
        except Exception as e:
            messages.error(request, f"Error al guardar el usuario: {e}")
            return render(request, 'miapp/insertarUsuario.html')

    return render(request, 'miapp/insertarUsuario.html')

def crearUsuarioCoordinador(request):
    if request.method == 'POST': 
        print(request.POST)  # Para depurar

        try:
            # Obtener los valores del formulario
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            dni = request.POST['dni']
            telefono = request.POST['telefono']
            email = request.POST['email']
            direccion = request.POST['direccion']
            ciudad = request.POST['ciudad']
            password = request.POST.get('password', 'default_password')  # Valor por defecto

            # Obtener el archivo de imagen, si está presente
            imagen = request.FILES.get('imagen', None)

            # Verificar si el email o el DNI ya existen en la base de datos
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
                return render(request, 'miapp/crearUsuarioCoordinador.html', {'form': request.POST})

            if Usuario.objects.filter(dni=dni).exists():
                messages.error(request, 'Ya existe un usuario con ese DNI.')
                return render(request, 'miapp/crearUsuarioCoordinador.html', {'form': request.POST})

            # Verificar si la casilla de "coordinador" está marcada
            is_coordinador = 'is_coordinador' in request.POST

            # Crear y guardar el usuario con la contraseña encriptada
            usuario = Usuario(
                nombre=nombre,
                apellidos=apellidos,
                dni=dni,
                telefono=telefono,
                email=email,
                direccion=direccion,
                ciudad=ciudad,
                password=make_password(password),
                is_coordinador=is_coordinador,
                imagen=imagen  # Aquí se asigna la imagen si se ha subido
            )
            usuario.save()
            messages.success(request, f'Usuario creado correctamente con nombre: {usuario.nombre}')
            return redirect('listarUsuarios')
        
        # Mandar mensaje en el registro por si acaso algún dato único ya está siendo utilizado anteriormente
        except IntegrityError:
            messages.error(request, "Error: Ya existe un usuario con ese email o DNI.")
            return render(request, 'miapp/crearUsuarioCoordinador.html')

        # Capturar cualquier otra excepción
        except Exception as e:
            messages.error(request, f"Error al guardar el usuario: {e}")
            return render(request, 'miapp/crearUsuarioCoordinador.html')

    return render(request, 'miapp/crearUsuarioCoordinador.html')

    
#@login_required
def crear_usuario_dentro_proyecto(request):
    if request.method == 'POST': 
        try:
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            dni = request.POST['dni']
            telefono = request.POST['telefono']
            email = request.POST['email']
            direccion = request.POST['direccion']
            ciudad = request.POST['ciudad']
            password = request.POST.get('password', 'default_password')

            # Verificar si la casilla de "coordinador" está marcada
            is_coordinador = 'is_coordinador' in request.POST

            # Crear y guardar el usuario con la contraseña encriptada
            usuario = Usuario(
                nombre=nombre,
                apellidos=apellidos,
                dni=dni,
                telefono=telefono,
                email=email,
                direccion=direccion,
                ciudad=ciudad,
                password=make_password(password), #importamos make_password
                is_coordinador=is_coordinador  # Asignar si es coordinador o no
            )
            usuario.save()
            messages.success(request, f'Usuario credo correctamente con nombre:{usuario.nombre} ')
            return redirect('inicio')
        except IntegrityError as e:
            error_message = "Error: Ya existe un usuario con ese email o DNI."
            print(error_message, e)
        except Exception as e:
            error_message = f"Error al guardar el usuario: {e}"
            print(error_message)

        return render(request, 'miapp/crearUsuarioDentrodeApp.html', {'error_message': error_message})

    return render(request, 'miapp/crearUsuarioDentrodeApp.html')

#Método para listar usuarios
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    
    return render(request, 'miapp/usuarios.html', {'usuarios': usuarios})

def listado_usuarios(request):
    # Obtén todos los usuarios
    usuarios = Usuario.objects.all()  # Si usas un modelo personalizado, cámbialo por el nombre de tu modelo
    return render(request, 'miapp/actividadesUsuarios.html', {'usuarios': usuarios})

#Metodo para borrar el usuario, tenemos en cuenta el id que será el que nos ayude a borrarlo
def borrar_usuario(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
        usuario.delete()# Eliminar el usuario
        messages.success(request, f"El usuario {usuario.nombre} ha sido eliminado correctamente")
        return redirect('listarUsuarios')  # Redirigir a la lista de usuarios
    except ValueError:
        raise Http404("Usuario no encontrado")  # Mostrar un error 404 si el usuario no existe

def editar_usuario(request, id):
    try:
        usuario = get_object_or_404(Usuario, id=id)

    except Usuario.DoesNotExist:
        return render(request, 'miapp/error.html', {'error': 'El usuario no existe'})

    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre', usuario.nombre) # Añadido
        usuario.email = request.POST.get('email', usuario.email) # Añadido
        usuario.apellidos = request.POST.get('apellidos', usuario.apellidos)  # Añadido
        usuario.dni = request.POST.get('dni', usuario.dni)  # Añadido
        usuario.telefono = request.POST.get('telefono', usuario.telefono)  # Añadido
        usuario.ciudad = request.POST.get('ciudad', usuario.ciudad)  # Añadido
        usuario.direccion = request.POST.get('direccion', usuario.direccion)  # Añadido
        usuario.save()
        return redirect('listarUsuarios')


    return render(request, 'miapp/usuario.html', {'usuario': usuario})

#Relacion de método entre usuario y evento: 
def eventos_usuario(request, user_id):
    try:
        # Obtener el usuario por su ID, pero usando el modelo 'Usuario' en lugar de 'User'
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Si el usuario no existe, redirigir o mostrar un error
        return render(request, 'miapp/error.html', {'mensaje': 'Usuario no encontrado'})

    # Obtener los eventos en los que el usuario está inscrito
    eventos = usuario.evento_set.all()  # Usamos la relación inversa para obtener los eventos

    if not eventos:
        # Si no hay eventos, pasar un mensaje adicional a la plantilla
        return render(request, 'miapp/error.html', {'mensaje': 'Este usuario no tiene eventos inscritos.'})

    # Pasar los eventos a la plantilla si hay
    return render(request, 'miapp/eventos_usuario.html', {'usuario': usuario, 'eventos': eventos})

#Métodos de los eventos

def ingresar_evento(request):
    if request.method == 'POST':
        try:
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            direccion = request.POST['direccion']
            fecha_realizacion = datetime.strptime(request.POST['fechaRealizacion'], '%Y-%m-%d').date()
            fecha_inscripcion = datetime.strptime(request.POST['fechaInscripcion'], '%Y-%m-%d').date()
            fecha_cierre = datetime.strptime(request.POST['fechaCierre'], '%Y-%m-%d').date()
            hora = datetime.strptime(request.POST['hora'], '%H:%M').time()
            precio = int(request.POST['precio'])
            numParticipantes = int(request.POST['numParticipantes'])
            categoria = request.POST['categoria']  # Nueva categoría
            print(f"Categoría recibida: {categoria}")  # Agregar para verificar el valor
            imagen = request.FILES.get('imagen')

            evento = Evento(
                nombre=nombre,
                descripcion=descripcion,
                direccion=direccion,
                fechaRealizacion=fecha_realizacion,
                fechaInscripcion=fecha_inscripcion,
                fechaCierre=fecha_cierre,
                hora=hora,
                precio=precio,
                numParticipantes=numParticipantes,
                categoria=categoria,
                imagen=imagen
            )
            evento.save()
            # Condición para redirigir según la categoría
            if categoria == 'deportivo':
                return redirect('listarEventos')
            
            if categoria == 'cultural':
                return redirect('listarEventosFiltrados', categoria=categoria)
        except Exception as e:
            print(f"Error al guardar el evento: {e}")

    return render(request, 'miapp/evento.html')


def listar_eventos(request, categoria=None):
    # Si la categoría es 'deportivo', renderiza la plantilla listadoEventos.html
    if categoria == 'deportivo':
        eventos = Evento.objects.filter(categoria='deportivo')
        return render(request, 'miapp/listadoEventos.html', {
            'eventos': eventos,
        })
    
    # Si la categoría es 'cultural', renderiza otra plantilla
    if categoria == 'cultural':
        eventos = Evento.objects.filter(categoria='cultural')
        return render(request, 'miapp/listadoEventosCulturales.html', {
            'eventos': eventos,
        })
    
    # Si no hay categoría, no hace nada
    return render(request, 'miapp/listadoEventos.html', {
        'eventos': Evento.objects.all(),
    })



def borrar_evento(request, id):
    try:
        evento = Evento.objects.get(id=id)
        evento.delete()  # Eliminar el usuario
        return redirect('listarEventos')  # Redirigir a la lista de usuarios
    except ValueError:
        raise Http404("Evento no encontrado")  # Mostrar un error 404 si el usuario no existe

def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)

    if request.method == 'POST':
        evento.nombre = request.POST.get('nombre', evento.nombre)
        evento.descripcion = request.POST.get('descripcion', evento.descripcion)
        evento.direccion = request.POST.get('direccion', evento.direccion)
        evento.fechaRealizacion = request.POST.get('fechaRealizacion', evento.fechaRealizacion)
        evento.fechaInscripcion = request.POST.get('fechaInscripcion', evento.fechaInscripcion)
        evento.fechaCierre = request.POST.get('fechaCierre', evento.fechaCierre)
        evento.hora = request.POST.get('hora', evento.hora)
        evento.precio = request.POST.get('precio', evento.precio)
        evento.numParticipantes = request.POST.get('numParticipantes', evento.numParticipantes)
        evento.categoria = request.POST.get('categoria', evento.categoria)

        if request.FILES.get('imagen'):
            evento.imagen = request.FILES['imagen']

        evento.save()
        return redirect('listarEventos')

    return render(request, 'miapp/editarEvento.html', {'evento': evento})


def ver_evento(request, id):
    try:
        evento = get_object_or_404(Evento, id=id)
    except Evento.DoesNotExist:
        return render(request, 'miapp/error.html', {'error': 'El evento no existe'})

    if request.method == 'POST':
        evento.nombre = request.POST.get('nombre', evento.nombre)
        
        # Para ver la imagen
        if request.FILES.get('imagen'):
            evento.imagen = request.FILES['imagen']

        evento.save()
        return redirect('listarEventos')  # Redirige a la lista de eventos

    return render(request, 'miapp/verEvento.html', {'evento': evento})

User = apps.get_model(settings.AUTH_USER_MODEL)  # Obtener el modelo de usuario correcto

#Métodos para los eventos y los usuarios, métodos para poder gestionar el coordinador los eventos.

#Realizar inscripción en un evento
@login_required
def inscribir_en_evento(request, categoria=None):
    print(f"Categoría recibida: {categoria}")  # Para ver si la categoría se pasa correctamente

    if categoria is None:
        categoria = 'deportivo'  # Esto asigna 'deportivo' por defecto

    # Filtrar los eventos según la categoría (deportivo o cultural)
    if categoria == 'deportivo':
        eventos = Evento.objects.filter(categoria='deportivo')
    elif categoria == 'cultural':
        eventos = Evento.objects.filter(categoria='cultural')
    else:
        eventos = Evento.objects.all()  # Si no se pasa ninguna categoría, muestra todos los eventos

    if request.method == 'POST':
        evento_id = request.POST.get('evento_id')
        usuario_id = request.POST.get('usuario_id')

        evento = get_object_or_404(Evento, id=evento_id)
        usuario = get_object_or_404(Usuario, id=usuario_id)

        fecha_actual = localdate()  # Obtiene la fecha actual

        if fecha_actual < evento.fechaInscripcion:
            mensaje = f"Las inscripciones para el evento {evento.nombre} aún no han comenzado."
        elif fecha_actual > evento.fechaCierre:
            mensaje = f"Las inscripciones para el evento {evento.nombre} ya han cerrado."
        else:
            if usuario not in evento.usuarios.all():
                evento.usuarios.add(usuario)
                evento.save()
                mensaje = f"{usuario.nombre} {usuario.apellidos} se ha inscrito con éxito en el evento {evento.nombre}."
            else:
                mensaje = f"{usuario.nombre} {usuario.apellidos} ya está inscrito en el evento {evento.nombre}."

        return render(request, 'miapp/inscripcion.html', {'mensaje': mensaje})

    usuarios = Usuario.objects.all()  # Obtener los usuarios

    return render(request, 'miapp/inscribir_en_evento.html', {
        'eventos': eventos,
        'usuarios': usuarios,
        'categoria': categoria
    })


#Listar participantes en los eventos:
@login_required
def lista_eventos_con_inscritos(request, categoria=None):
    # Imprimir el valor de la categoría para depuración
    print(f"Categoría recibida: {categoria}")

    # Si no se pasa ninguna categoría, se establece 'deportivo' como valor por defecto
    if categoria is None:
        categoria = 'deportivo'  # Categoría por defecto

    # Filtrar eventos según la categoría
    if categoria == 'deportivo':
        eventos = Evento.objects.prefetch_related('usuarios').filter(categoria='deportivo')
    elif categoria == 'cultural':
        eventos = Evento.objects.prefetch_related('usuarios').filter(categoria='cultural')
    else:
        eventos = Evento.objects.prefetch_related('usuarios').all()  # Si no coincide, mostrar todos

    return render(request, 'miapp/lista_eventos_con_usuarios.html', {
        'eventos': eventos,
        'categoria': categoria
    })


#Cancelar inscripción en un evento:
@login_required
def cancelar_inscripcion_en_evento(request):
    if request.method == 'POST':
        evento_id = request.POST.get('evento_id')
        evento = get_object_or_404(Evento, id=evento_id)
        usuario = request.user
        if usuario in evento.usuarios.all():
            evento.usuarios.remove(usuario)
            evento.save()
            mensaje = f"Has cancelado tu inscripción en el evento {evento.nombre}."
        else:
            mensaje = f"No estabas inscrito en el evento {evento.nombre}."
        return render(request, 'inscripcion.html', {'mensaje': mensaje})
    else:
        eventos = Evento.objects.filter(usuarios=request.user)
        return render(request, 'cancelar_inscripcion_evento.html', {'eventos': eventos})

def ingresar_mensaje(request):
    if request.method == 'POST':
        try:
            nombre = request.POST['nombre']
            email = request.POST['email']
            texto = request.POST['texto']
            
            # Crear y guardar el mensaje
            mensaje = Mensajes(
                nombre=nombre,
                email=email,
                texto=texto,
            )
            mensaje.save()
            print(f"Mensaje guardado: {mensaje}")  # Verificación en la consola
            return redirect('mensaje')  # Redireccionar después de guardar
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")

    return render(request, 'miapp/mensaje.html')

def borrar_mensaje(request, id):
    try:
        mensaje = Mensajes.objects.get(id=id)
        mensaje.delete()  # Eliminar el mensaje
        return redirect('listar_mensajes')  # Redirigir a la lista de mensajes
    except ValueError:
        raise Http404("Mensaje no encontrado")  # Mostrar un error 404 si el mensaje no existe


def listar_mensajes(request):
    mensajes = Mensajes.objects.all()  # Obtiene todos los mensajes de la base de datos
    
    return render(request, 'miapp/mensaje.html', {'mensajes': mensajes})  # Clave en minúsculas

#Insertar mensaje para sugerencias de usuarios  

#Métodos ligados a insertar el pago


