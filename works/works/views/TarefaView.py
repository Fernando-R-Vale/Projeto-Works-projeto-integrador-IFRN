from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from works.decorators import lider_required, planejador_required, any_role_required
from works.models import Tarefa, Planejador, Lider, Colaborador, TarefaColaborador
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
import datetime


@planejador_required
def list_tarefas_view(request):
    query = request.GET.get('query')
    if query:
        tarefas = Tarefa.objects.filter(id__icontains=query)  # Filtra por id
    else:
        tarefas = Tarefa.objects.all()
    tarefa = request.GET.get("tarefa")
    if tarefa is not None:
        tarefas = tarefas.filter(tarefa__contains=tarefa)
    context = {'tarefas': tarefas}
    return render(request, template_name='tarefa/tarefa-details.html', context=context, status=200)

@planejador_required
def tarefa_edit(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)
    colaboradores = Colaborador.objects.all()
    
    # Obter colaboradores atuais desta tarefa
    current_colaboradores = tarefa.tarefacolaborador_set.select_related('colaborador').all()
    current_cpfs = set(tc.colaborador.cpf for tc in current_colaboradores)
    
    if request.method == "POST":
        try:
            # Atualizar dados básicos
            tarefa.nome = request.POST.get("nome", tarefa.nome)
            tarefa.descricao = request.POST.get("descricao", tarefa.descricao)
            
            # Atualizar líder
            lider_id = request.POST.get("lider_id")
            if lider_id:
                tarefa.lider_email = Lider.objects.get(email=lider_id)
            
            tarefa.save()

            # Processar colaboradores
            novos_cpfs = set(request.POST.getlist('colaboradores'))
            
            # Identificar relações para remover
            to_remove = current_cpfs - novos_cpfs
            tarefa.tarefacolaborador_set.filter(colaborador__cpf__in=to_remove).delete()
            
            # Identificar colaboradores para adicionar
            to_add = novos_cpfs - current_cpfs
            for cpf in to_add:
                colaborador = Colaborador.objects.get(cpf=cpf)
                TarefaColaborador.objects.create(tarefa=tarefa, colaborador=colaborador)

            messages.success(request, "Tarefa atualizada com sucesso!")
            return redirect('tarefa-details')

        except Lider.DoesNotExist:
            messages.error(request, "Líder selecionado não encontrado!")
        except Colaborador.DoesNotExist as e:
            messages.error(request, f"Colaborador não encontrado: {str(e)}")
        except Exception as e:
            messages.error(request, f"Erro ao atualizar tarefa: {str(e)}")
        
        return redirect('tarefa-edit', id=id)

    context = {
        'tarefa': tarefa,
        'lideres': Lider.objects.all(),
        'colaboradores': colaboradores,
        'colaboradores_selecionados': [tc.colaborador for tc in current_colaboradores]
    }
    return render(request, 'tarefa/tarefa-edit.html', context)

@planejador_required
def create_tarefas_view(request):
    if 'user_email' not in request.session or request.session.get('user_type') != 'planejador':
        messages.error(request, "Você precisa estar logado como planejador para acessar esta página.")
        return redirect('login')
    
    lideres = Lider.objects.all()
    colaboradores = Colaborador.objects.all()  # Novo

    if request.method == 'POST':
        try:
            # Coletar dados do formulário
            nome = request.POST.get('nome')
            descricao = request.POST.get('descricao')
            lider_id = request.POST.get('lider_id')
            colaboradores_ids = request.POST.getlist('colaboradores')  # Novo
            dh_inicio = request.POST.get('dh_inicio') or timezone.now()
            dh_termino = request.POST.get('dh_termino') or timezone.now()

            # Validações básicas
            if not all([nome, lider_id]):
                messages.error(request, "Campos obrigatórios não preenchidos!")
                return redirect('tarefa-create')

            planejador = Planejador.objects.get(email=request.session['user_email'])
            lider = Lider.objects.get(email=lider_id)

            # Criar tarefa
            tarefa = Tarefa.objects.create(
                status='Pendente',
                nome=nome,
                descricao=descricao,
                planejador_email=planejador,
                lider_email=lider,
                dh_inicio=dh_inicio,
                dh_termino=dh_termino
            )

            # Adicionar colaboradores (Novo)
            for cpf in colaboradores_ids:
                colaborador = Colaborador.objects.get(cpf=cpf)
                TarefaColaborador.objects.create(tarefa=tarefa, colaborador=colaborador)

            messages.success(request, "Tarefa criada com sucesso!")
            return redirect('tarefa-details')

        except Lider.DoesNotExist:
            messages.error(request, "Líder selecionado não encontrado!")
        except Colaborador.DoesNotExist:  # Novo
            messages.error(request, "Colaborador selecionado não encontrado!")
        except Exception as e:
            messages.error(request, f"Erro ao criar tarefa: {str(e)}")
        
        return redirect('tarefa-create')

    context = {
        'lideres': lideres,
        'colaboradores': colaboradores  # Novo
    }
    return render(request, 'tarefa/tarefa-create.html', context)


@lider_required
def registro_tarefa_view(request,id):
    print("registro_tarefa_view")
    tarefa = get_object_or_404(Tarefa, id=id)
    print(tarefa)
    if request.method == 'POST':
        print("POST")
        tarefa.ocorrencia = request.POST.get('ocorrencia')
        print(tarefa.ocorrencia)
        tarefa.dh_inicio = request.POST.get('data_inicio')
        print(request.POST.get('data_inicio'))
        tarefa.dh_termino = request.POST.get('data_fim')
        print(tarefa.dh_termino)
        tarefa.status = request.POST.get('status')
        tarefa.cadastro_realizado = True
        tarefa.save()

        return redirect('home-lider')

    return render(request, 'tarefa/registro-tarefas.html', {'tarefa': tarefa})

@lider_required
def editar_registrar_view(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)
    
    # Verificação adicional de segurança
    if not tarefa.cadastro_realizado:
        return redirect('home-lider')

    if request.method == "POST":
        tarefa.ocorrencia = request.POST.get("ocorrencia")
        tarefa.status = request.POST.get("status")
        tarefa.dh_inicio = request.POST.get("data_inicio")
        tarefa.dh_termino = request.POST.get("data_fim")
        tarefa.save()
        return redirect("home-lider")  

    return render(request, "tarefa/registro-tarefas-editar.html", {"tarefa": tarefa})

@lider_required
def home_lider_view(request):
    if 'user_email' not in request.session or request.session.get('user_type') != 'lider':
        return redirect('login')

    try:
        lider = Lider.objects.get(email=request.session['user_email'])
    except Lider.DoesNotExist:
        return redirect('login')

    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', 'dh_inicio')
    cadastro_filter = request.GET.get('cadastro', '')

    tarefas = Tarefa.objects.filter(lider_email=lider)


    if search_query:
        tarefas = tarefas.filter(
            Q(nome__icontains=search_query) | 
            Q(descricao__icontains=search_query)
        )
    
    if status_filter:
        tarefas = tarefas.filter(status=status_filter)
    
    if cadastro_filter:
        tarefas = tarefas.filter(cadastro_realizado=(cadastro_filter == 'true'))

    tarefas = tarefas.order_by(sort_by)

    context = {
        'tarefas': tarefas,
        'user_name': lider.nome,
        'current_search': search_query,
        'current_status': status_filter,
        'current_sort': sort_by,
        'current_cadastro': cadastro_filter
    }
    return render(request, 'tarefa/home-lider.html', context=context, status=200)

@planejador_required
def tarefa_delete(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)
    tarefa.delete()
    return redirect("tarefa-details")

@any_role_required(allowed_roles=['lider', 'planejador'])
def visualizar_tarefa_view(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)
    colaboradores = tarefa.tarefacolaborador_set.all().select_related('colaborador')
    
    status_display = {
        'pendente': 'Pendente',
        'em_andamento': 'Em Andamento', 
        'concluido': 'Concluído'
    }
    
    context = {
        'tarefa': tarefa,
        'status_display': status_display,
        'colaboradores': [tc.colaborador for tc in colaboradores],
        'user_type': request.session.get('user_type')
    }
    return render(request, 'tarefa/visualizar-tarefa.html', context)