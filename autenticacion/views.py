from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.db.models import Q
from academico.models import Usuario
from .hashers import verificar_password


class LoginView(View):
    template_name = 'autenticacion/login.html'

    def get(self, request):
        if request.session.get('usuario_id'):
            return redirect('academico:lista_cursos')

        logout_exitoso = request.GET.get('logout') == '1'
        return render(request, self.template_name, {'logout': logout_exitoso})

    def post(self, request):
        try:
            identificador = request.POST.get('identificador', '').strip()
            password = request.POST.get('password', '').strip()

            if not identificador or not password:
                return render(request, self.template_name, {
                    'error': 'Debes ingresar tu usuario/correo y contraseña.'
                })

            # Busca por username O por correo, lo que el usuario haya escrito
            usuario = Usuario.objects.filter(
                Q(username=identificador) | Q(correo=identificador)
            ).first()

            if not usuario:
                return render(request, self.template_name, {
                    'error': 'Usuario o contraseña incorrectos.'
                })

            if not verificar_password(password, usuario.contrasena):
                return render(request, self.template_name, {
                    'error': 'Usuario o contraseña incorrectos.'
                })

            if usuario.estado != 'activo':
                return render(request, self.template_name, {
                    'error': 'Tu cuenta está inactiva. Contacta al administrador.'
                })

            request.session['usuario_id'] = usuario.id_usuario
            request.session['usuario_nombre'] = usuario.primer_nombre
            request.session['usuario_rol'] = usuario.rol

            return redirect('academico:lista_cursos')

        except Exception as e:
            print(f"DEBUG: Error en LoginView - {e}")  # útil para debug, lo quitas después
            return render(request, self.template_name, {
                'error': 'Ocurrió un error al iniciar sesión. Intenta de nuevo.'
            })


class LogoutView(View):
    def post(self, request):
        try:
            request.session.flush()
        except Exception as e:
            print(f"DEBUG: Error en LogoutView - {e}")
        return redirect(f"{reverse('autenticacion:login')}?logout=1")

    def get(self, request):
        try:
            request.session.flush()
        except Exception as e:
            print(f"DEBUG: Error en LogoutView - {e}")
        return redirect(f"{reverse('autenticacion:login')}?logout=1")