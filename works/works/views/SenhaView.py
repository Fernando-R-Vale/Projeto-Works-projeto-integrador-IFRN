from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
import random
from works.models import Planejador, Lider
from django.contrib.auth.hashers import make_password
def digitar_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        codigo = random.randint(100000, 999999)  # Gera um código de 6 dígitos
        
        # Verificar se o email pertence a um Planejador ou Líder
        try:
            usuario = Planejador.objects.get(email=email)
        except Planejador.DoesNotExist:
            try:
                usuario = Lider.objects.get(email=email)
            except Lider.DoesNotExist:
                usuario = None
        
        if usuario:
            # Enviar o email
            send_mail(
                'Código de Recuperação de Senha',
                f'Seu código de recuperação de senha é: {codigo}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            # Salvar o código na sessão do usuário para verificação futura
            request.session['codigo_recuperacao'] = codigo
            request.session['email_recuperacao'] = email
            return redirect('verificar-codigo')
        else:
            messages.error(request, 'E-mail não encontrado. Verifique e tente novamente.')
    return render(request, 'senha/digitar-email.html')



def verificar_codigo(request):
    if request.method == 'POST':
        codigo_inserido = request.POST['codigo']
        codigo_armazenado = request.session.get('codigo_recuperacao')
        if codigo_inserido == str(codigo_armazenado):
            return redirect('nova_senha')
        else:
            messages.error(request, 'Código incorreto. Tente novamente.')
    return render(request, 'senha/verificar-codigo.html')





def nova_senha(request):
    if request.method == 'POST':
        nova_senha = request.POST.get('newPassword')
        confirmar_senha = request.POST.get('confirmPassword')
        email = request.session.get('email_recuperacao')
        
        if nova_senha == confirmar_senha:
            # Verificar se o email pertence a um Planejador ou Líder
            try:
                usuario = Planejador.objects.get(email=email)
                usuario.senha = nova_senha  # Salva a senha em texto claro
                usuario.save()
                print("Senha atualizada para Planejador")
            except Planejador.DoesNotExist:
                try:
                    usuario = Lider.objects.get(email=email)
                    usuario.senha = nova_senha  # Salva a senha em texto claro
                    usuario.save()
                    print("Senha atualizada para Líder")
                except Lider.DoesNotExist:
                    usuario = None
                    print("Usuário não encontrado")

            if usuario:
                return redirect('recuperacao_sucesso')
            else:
                messages.error(request, 'Erro ao redefinir a senha. Tente novamente.')
        else:
            messages.error(request, 'As senhas não coincidem. Tente novamente.')
    return render(request, 'senha/nova-senha.html')



def recuperacao_sucesso(request):
    return render(request, 'senha/recuperacao-sucesso.html')
