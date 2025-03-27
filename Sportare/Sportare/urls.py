"""
URL configuration for Sportare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from miapp import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    #Path informacion, menú y de vista
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('contacto/', views.contacto, name='contacto'),
    path('servicio/', views.servicio, name='servicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('menu/', views.menu, name='menu'),
    path('menuUsuariosCoordinador/', views.menuUsuariosCoordinador, name="menuUsuariosCoordinador"),
    path('menuActividadesCoordinador/', views.menuActividadesCoordinador, name="menuActividadesCoordinador"),
    path('menuActividadesCulturalesCoordinador/', views.menuActividadesCulturalesCoordinador, name="menuActividadesCulturalesCoordinador"),
    path('evento/<int:id>/ver_evento/', views.ver_evento, name='ver_evento'),

    #Url Admin que pondremos con nuestra direccion
    path('admin/', admin.site.urls),
    #Path ligados a insertar:
    path('crearEvento1/', views.ingresar_evento, name='crear_evento'), 
    path('crearEvento1/', views.ingresar_evento, name='crearEvento1'),
    path('insertarUsuario/', views.crear_usuario, name='insertarUsuario'),
    path('registro/', views.register_user, name='registro'),
    path('crearUsuarioCoordinador/', views.crearUsuarioCoordinador, name="crearUsuarioCoordinador"),
    path('createUsuario', views.crear_usuario_dentro_proyecto, name='crear_usuario_dentro_proyecto'), #creamos usuario restringido dentro de app
    
    #Path para que el coordinador ingrese o vea un usuario en una actividad
    path('inscribir/<str:categoria>/', views.inscribir_en_evento, name='inscribir_en_evento'),
    path('inscribir/', views.inscribir_en_evento, name='inscribir_en_evento'),
    path('mensaje/', views.ingresar_mensaje, name='mensaje'),  

    #path('lista_eventos/', views.lista_eventos_con_inscritos, name='lista_eventos'), 
    path('lista_eventos/<str:categoria>/', views.lista_eventos_con_inscritos, name='lista_eventos'),


    #Path ligados al login y logout (cierre de sesión)
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_out, name='logout'),
    
    #Path ligadas a listar
    path('listarUsuarios/', views.listar_usuarios, name='listarUsuarios'),
    path('listarEventos/', views.listar_eventos, name="listarEventos"),
    path('listarEventos/<str:categoria>/', views.listar_eventos, name="listarEventosFiltrados"),
    path('listado_usuarios/', views.listado_usuarios, name='listado_usuarios'),
    path('listar_mensajes/', views.listar_mensajes, name='listar_mensajes'),
    path('listar_mensajes/', views.listar_mensajes, name='listar_mensajes'),
    
    #Path ligados a borrar
    path('borrar-usuario/<int:id>/', views.borrar_usuario, name='borrar'),
    path('borrar-evento/<int:id>/', views.borrar_evento, name='borrar_evento'),
    path('borrar_mensaje/<int:id>/', views.borrar_mensaje, name='borrar_mensaje'),
    
    #Path ligados a editar
    path('usuario/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('editarEvento/<int:id>/', views.editar_evento, name='editarEvento'),
    #Path ligado a la relación usuario/evento:
    path('usuario/<int:user_id>/eventos/', views.eventos_usuario, name='eventos_usuario'),
    
    



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Configuracion para cargar las imagenes
admin.site.site_header = "Sportare" #Con esto voy a cambiar el nombre del panel de administración
admin.site.site_title = "Sportare" #Con esto cambio el nombre de la web
admin.site.index_title= "Panel de gestión" #Con esto cambio el index