from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path("", views.inicio , name="home"),
    path("login", views.login_request , name="Login"),
    path("register", views.register , name="Register"),
    path("logout" , LogoutView.as_view(template_name="logout.html") , name="logout"),
    path("editarPerfil" , views.editarPerfil , name="EditarPerfil"),
    path("inicio", views.inicio_sesion , name="incio"),

    
    path("ver_cursos", views.ver_cursos , name="cursos"),
    path("curso_formulario", views.curso_formulario, name="altas_cursos"),
    path("elima_curso/<int:id>", views.elimina_curso, name ="elimina_curso"),
    path("editar_curso/<int:id>" , views.editar_curso , name="editar_curso"),
    path("buscar_curso" , views.buscar_curso, name="buscar_curso" ),
    path("buscar_c" , views.buscar_c),
    


    path("ver_alumnos", views.ver_alumnos , name="alumnos"),
    path("alumno_formulario", views.alumno_formulario, name="altas_alumnos"),
    path("elima_alumno/<int:id>", views.elimina_alumno, name ="elimina_alumno"),
    path("editar_alumno/<int:id>" , views.editar_alumno , name="editar_alumno"),
    path("buscar_alumno" , views.buscar_alumno, name="buscar_alumno" ),
    path("buscar_a" , views.buscar_a),


    path("ver_profesores", views.ver_profesores , name="profesores"),
    path("profesor_formulario", views.profesor_formulario, name="altas_profesores"),
    path("elima_profesor/<int:id>", views.elimina_profesor, name ="elimina_profesor"),
    path("editar_profesor/<int:id>" , views.editar_profesor , name="editar_profesor"),
    path("buscar_profesor" , views.buscar_profesor, name="buscar_profesor" ),
    path("buscar_p" , views.buscar_p),

    

]