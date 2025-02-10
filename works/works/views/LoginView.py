from django.shortcuts import render, redirect
from django.contrib import messages
from works.models import Lider, Planejador

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        # Verificar se é um líder
        user_lider = Lider.objects.filter(email=email, senha=senha).first()
        if user_lider:
            print("teste")
            request.session['user_email'] = user_lider.email  # Cria a sessão para o líder
            request.session['user_type'] = 'lider'  # Tipo de usuário: lider
            print("teste")
            return redirect('home-lider')

        # Verificar se é um planejador
        user_planejador = Planejador.objects.filter(email=email, senha=senha).first()
        if user_planejador:
            request.session['user_email'] = user_planejador.email  # Cria a sessão para o planejador
            request.session['user_type'] = 'planejador'  # Tipo de usuário: planejador
            return redirect('home')

        # Se não encontrar, mostrar erro
        messages.error(request, 'E-mail ou senha incorretos.')

    return render(request, 'login.html')
def logout(request):
    # Limpar a sessão
    request.session.flush()  # Remove todos os dados da sessão
    return redirect('login')