from django.shortcuts import redirect

class LoginRequeridoMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('autenticacion:login')
        return super().dispatch(request, *args, **kwargs)