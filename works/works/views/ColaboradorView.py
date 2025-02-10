from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from works.models import Colaborador
from django.http import HttpResponse
from datetime import datetime
import os
from django.conf import settings
from works.decorators import planejador_required


@planejador_required
def list_colaboradores(request):
    query = request.GET.get('query')
    if query:
        colaboradores = Colaborador.objects.filter(nome__icontains=query)  # Filtra por nome
    else:
        colaboradores = Colaborador.objects.all()
    colaborador = request.GET.get("colaborador")
    if colaborador is not None:
        colaboradores = colaboradores.filter(Colaborador__contains=colaborador)
    context = {'colaboradores': colaboradores}
    return render(request, template_name='colaborador/colaborador-manage.html', context=context, status=200)


@planejador_required
def create_colaborador_view(request):
    print("colaborador_view")
    if request.method == 'POST':
        print("colaborador_view POST")
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        dt_nascimento = request.POST.get("dt_nascimento")
        profissao = request.POST.get("profissao")
        descricao = request.POST.get("descricao")
        foto = request.POST.get("foto")
        
        try:
            # Validando os campos obrigatórios
            if not nome or not cpf or not dt_nascimento or not profissao:
                raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")

            # Convertendo data para o formato adequado
            from datetime import datetime
            dt_nascimento = datetime.strptime(dt_nascimento, "%Y-%m-%d").date()
            
            # Criando o objeto Colaborador
            colaborador = Colaborador()
            colaborador.nome = nome
            colaborador.cpf = cpf
            colaborador.dt_nascimento = dt_nascimento
            colaborador.profissao = profissao
            colaborador.descricao = descricao
            if request.FILES is not None:
                num_files = len(request.FILES.getlist('foto'))
                if num_files > 0:
                    imagefile = request.FILES['foto']
                    print(imagefile)
                    fs = FileSystemStorage()
                    filename = fs.save(imagefile.name, imagefile)
                    if (filename is not None) and (filename != ""):
                        colaborador.foto = filename
            
            colaborador.save()
            print(f"Colaborador {nome} salvo com sucesso!")

        except Exception as e:
            print(f"Erro ao salvar colaborador: {e}")
        return redirect("colaborador-create")

    return render(request, template_name="colaborador/colaborador-create.html", status=200)


@planejador_required
def list_colaborador_view(request):
    colaboradores = list(range(9))
    context = {'colaboradores': colaboradores}
    return render(request, template_name='colaborador/colaborador-details.html', context=context, status=200)


@planejador_required
def colaborador_edit(request, cpf):
    # Verifica se o CPF foi passado corretamente
    print(f"CPF recebido: {cpf}")
    colaborador = get_object_or_404(Colaborador, cpf=cpf)

    if request.method == "POST":
        # Recebendo dados do formulário
        nome = request.POST.get("nome")
        dt_nascimento = request.POST.get("dt_nascimento")
        cpf = request.POST.get("cpf")
        profissao = request.POST.get("profissao")
        descricao = request.POST.get("descricao")
        foto = request.FILES.get("foto")

        try:
            # Atualizando campos
            colaborador.nome = nome if nome else colaborador.nome  # Mantém o nome anterior se não for enviado
            # Verifica se a data de nascimento foi fornecida
            if dt_nascimento:
                colaborador.dt_nascimento = datetime.strptime(dt_nascimento, "%Y-%m-%d").date()
            else:
                # Se não for fornecida, mantém a data anterior
                colaborador.dt_nascimento = colaborador.dt_nascimento

            colaborador.cpf = cpf if cpf else colaborador.cpf  # Mantém o CPF anterior se não for enviado
            colaborador.profissao = profissao if profissao else colaborador.profissao  # Mantém a profissão anterior se não for enviada
            colaborador.descricao = descricao if descricao else colaborador.descricao  # Mantém a descrição anterior se não for enviada

            # Verifica se uma nova foto foi fornecida
            if foto:
                colaborador.foto = foto
            # Se não, mantém a foto anterior

            colaborador.save()
            print(f"Colaborador {nome} atualizado com sucesso!")
            return redirect('colaborador-manage')

        except Exception as e:
            print(f"Erro ao atualizar colaborador: {e}")
            return HttpResponse("Erro ao salvar colaborador", status=400)

    return render(request, 'colaborador/colaborador-edit.html', {'colaborador': colaborador})

@planejador_required
def colaborador_delete(request, cpf):
    colaborador = get_object_or_404(Colaborador, cpf=cpf)
    foto_path = colaborador.foto.path
        
    if os.path.exists(foto_path):
        print(colaborador.foto.path)
        os.remove(foto_path)  
    
    colaborador.delete()
    return redirect("colaborador-manage")