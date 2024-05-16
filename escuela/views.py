from django.shortcuts import render
from escuela.models import Curso, Alumno, Profesor, Avatar
from django.http import HttpResponse
from django.template import loader
from escuela.forms import Curso_formulario, Alumno_formulario, Profesor_formulario, UserEditForm
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def inicio(request):
    if request.user.is_authenticated:
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request , "home.html", {"url":avatares[0].imagen.url if avatares.exists() else None})
    else:
        return render(request , "home.html")
    

def inicio_sesion(request):
    if request.user.is_authenticated:
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request , "inicio.html", {"url":avatares[0].imagen.url if avatares.exists() else None})
    else:
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request , "inicio.html", {"url":avatares[0].imagen.url if avatares.exists() else None})

#--------------------------loging--------------------------------------


def login_request(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            user = authenticate(username=usuario , password=contra)
            if user is not None:
                login(request , user )
                avatares = Avatar.objects.filter(user=request.user.id)
                return render( request , "inicio.html" , {"url":avatares[0].imagen.url if avatares.exists() else None, "usuario":usuario, "mensaje":f"Bienvenido/a {usuario}"})
            else:
                return HttpResponse(f"Usuario no encontrado")
        else:
            return HttpResponse(f"FORM INCORRECTO {form}")
    

    form = AuthenticationForm()
    return render( request , "login.html" , {"form":form})


#----------------------------registro------------------------------------

def register(request):

    if request.method == "POST":
        
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()

            return render( request , "login.html" )
        
            
    else:
        form = UserCreationForm()
    return render(request , "registro.html" , {"form":form})


#----------------------------editar usuario------------------------------------

def editarPerfil(request):

    usuario = request.user
    if request.method == "POST":
        mi_formulario = UserEditForm(request.POST)

        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            usuario.email = informacion["email"]
            password = informacion["password1"]
            usuario.set_password(password)
            avatares = Avatar.objects.filter(user=request.user.id)
            usuario.save()
            return render(request , "inicio.html", {"url":avatares[0].imagen.url if avatares.exists() else None})
        
    else:
        avatares = Avatar.objects.filter(user=request.user.id)
        miFormulario = UserEditForm(initial={'email':usuario.email})
    return render( request , "editar_perfil.html", {"miFormulario":miFormulario, "usuario":usuario, "url":avatares[0].imagen.url if avatares.exists() else None})


#----------------------------cursos------------------------------------



def ver_cursos(request):
    cursos = Curso.objects.all()
    if request.user.is_authenticated:
        avatares = Avatar.objects.filter(user=request.user.id)

        return render(request , "cursos.html", {"url":avatares[0].imagen.url if avatares.exists() else None, "cursos": cursos})
    return render(request , "cursos.html", {"cursos": cursos})
    

def curso_formulario(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method == "POST":

        mi_formulario = Curso_formulario( request.POST )
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso = Curso( nombre=datos["nombre"] , camada=datos["camada"])
            curso.save()
            
            return render(request , "curso_formulario.html", {"url":avatares[0].imagen.url if avatares.exists() else None})

    return render(request , "curso_formulario.html", {"url":avatares[0].imagen.url if avatares.exists() else None})


def elimina_curso(request , id ):

    curso = Curso.objects.get(id=id)
    curso.delete()
    curso = Curso.objects.all()

    return render(request , "cursos.html" , {"cursos":curso})


def editar_curso(request , id):

    curso = Curso.objects.get(id=id)
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method == "POST":
        mi_formulario = Curso_formulario( request.POST )
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso.nombre = datos["nombre"]
            curso.camada = datos["camada"]
            curso.save()
            curso = Curso.objects.all()
            
            return render(request , "cursos.html" , {"cursos":curso, "url":avatares[0].imagen.url if avatares.exists() else None})
    else:
        mi_formulario = Curso_formulario(initial={"nombre":curso.nombre , "camada":curso.camada})

    return render( request , "editar_curso.html" , {"mi_formulario": mi_formulario , "curso":curso, "url":avatares[0].imagen.url if avatares.exists() else None })



def buscar_curso(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "buscar_curso.html", {"url":avatares[0].imagen.url if avatares.exists() else None})
    


def buscar_c(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        cursos = Curso.objects.filter(nombre__icontains= nombre)
        return render( request , "resultado_busqueda.html" , {"cursos":cursos, "url":avatares[0].imagen.url if avatares.exists() else None})
    else:
        return HttpResponse("Ingrese el nombre del curso",{"url":avatares[0].imagen.url if avatares.exists() else None})



#----------------------------------alumno---------------------------------------------------



def ver_alumnos(request):
    alumnos = Alumno.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request , "alumnos.html", {"url":avatares[0].imagen.url if avatares.exists() else None, "alumnos": alumnos})

def alumno_formulario(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    alumnos = Alumno.objects.all()
    if request.method == "POST":

        mi_formulario = Alumno_formulario( request.POST )

        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            alumno = Alumno( nombre=datos["nombre"] , dni=datos["dni"])
            alumno.save()
            return render(request , "alumnos.html", {"url":avatares[0].imagen.url if avatares.exists() else None, "alumnos": alumnos})


    return render(request , "alumno_formulario.html", {"url":avatares[0].imagen.url if avatares.exists() else None})


def elimina_alumno(request , id ):

    avatares = Avatar.objects.filter(user=request.user.id)

    alumno = Alumno.objects.get(id=id)
    alumno.delete()
    alumno = Alumno.objects.all()

    return render(request , "alumnos.html" , {"alumnos":alumno,"url":avatares[0].imagen.url if avatares.exists() else None})




def editar_alumno(request , id):

    avatares = Avatar.objects.filter(user=request.user.id)

    alumno = Alumno.objects.get(id=id)
    
    if request.method == "POST":
        mi_formulario = Alumno_formulario( request.POST )
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            alumno.nombre = datos["nombre"]
            alumno.dni = datos["dni"]
            alumno.save()
            alumno = Alumno.objects.all()

            return render(request , "alumnos.html" , {"alumnos":alumno, "url":avatares[0].imagen.url if avatares.exists() else None})
    else:
        mi_formulario = Alumno_formulario(initial={"nombre":alumno.nombre , "dni":alumno.dni})

    return render( request , "editar_alumno.html" , {"mi_formulario": mi_formulario , "alumno":alumno, "url":avatares[0].imagen.url if avatares.exists() else None})



def buscar_alumno(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "buscar_alumno.html", {"url":avatares[0].imagen.url if avatares.exists() else None})
    


def buscar_a(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        alumnos = Alumno.objects.filter(nombre__icontains= nombre)
        return render( request , "resultados_busqueda_a.html" , {"alumnos":alumnos, "url":avatares[0].imagen.url if avatares.exists() else None})
    else:
        return HttpResponse("Ingrese el nombre del alumno",{"url":avatares[0].imagen.url if avatares.exists() else None})



#-------------------------------------profesor----------------------------------------------


def ver_profesores(request):
    profesores = Profesor.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request , "profesores.html", {"url":avatares[0].imagen.url if avatares.exists() else None, "profesores": profesores})



def profesor_formulario(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    profesores = Profesor.objects.all()
    if request.method == "POST":

        mi_formulario = Profesor_formulario( request.POST )

        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            profesor = Profesor( nombre=datos["nombre"] , dni=datos["dni"], curso=datos["curso"])
            profesor.save()
            return render(request , "profesores.html", {"url":avatares[0].imagen.url if avatares.exists() else None, "profesores": profesores})


    return render(request , "profesor_formulario.html", {"url":avatares[0].imagen.url if avatares.exists() else None})




def elimina_profesor(request , id ):

    avatares = Avatar.objects.filter(user=request.user.id)

    profesor = Profesor.objects.get(id=id)
    profesor.delete()
    profesor = Profesor.objects.all()

    return render(request , "profesores.html" , {"profesores":profesor,"url":avatares[0].imagen.url if avatares.exists() else None})




def editar_profesor(request , id):

    avatares = Avatar.objects.filter(user=request.user.id)

    profesor = Profesor.objects.get(id=id)
    
    if request.method == "POST":
        mi_formulario = Profesor_formulario( request.POST )
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            profesor.nombre = datos["nombre"]
            profesor.dni = datos["dni"]
            profesor.curso = datos["curso"]
            profesor.save()
            profesor = Profesor.objects.all()

            return render(request , "profesores.html" , {"profesores":profesor, "url":avatares[0].imagen.url if avatares.exists() else None})
    else:
        mi_formulario = Profesor_formulario(initial={"nombre":profesor.nombre , "dni":profesor.dni, "curso":profesor.curso})

    return render( request , "editar_profesor.html" , {"mi_formulario": mi_formulario , "profesor":profesor, "url":avatares[0].imagen.url if avatares.exists() else None})



def buscar_profesor(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "buscar_profesor.html", {"url":avatares[0].imagen.url if avatares.exists() else None})
    


def buscar_p(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        profesores = Profesor.objects.filter(nombre__icontains= nombre)
        return render( request , "resultado_busqueda_p.html" , {"profesores":profesores, "url":avatares[0].imagen.url if avatares.exists() else None})
    else:
        return HttpResponse("Ingrese el nombre del profesor",{"url":avatares[0].imagen.url if avatares.exists() else None})

