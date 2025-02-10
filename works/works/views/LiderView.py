from django.shortcuts import render, redirect, get_object_or_404
from works.decorators import planejador_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from works.models import Lider
import os
@planejador_required
def list_lideres(request):
    query = request.GET.get('query')
    if query:
        lideres = Lider.objects.filter(nome__icontains=query)  # Filtra por nome
    else:
        lideres = Lider.objects.all()
    lider = request.GET.get("lider")
    if lider is not None:
        lideres = lideres.filter(Lider__contains=lider)
    context = {'lideres': lideres}
    return render(request, template_name='lider/lider-manage.html', context=context, status=200)
@planejador_required
def create_lider_view(request):
    if request.method == 'POST':
        print("lider_view POST")
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        profissao = request.POST.get("profissao")
        foto = request.POST.get("foto")
        
        try:
            # Validando os campos obrigatórios
            if not nome or not email or not profissao or not senha:
                raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")
            
            # Criando o objeto lider
            lider = Lider()
            lider.nome = nome
            lider.email = email
            lider.senha = senha
            lider.profissao = profissao
            if request.FILES is not None:
                num_files = len(request.FILES.getlist('foto'))
                if num_files > 0:
                    imagefile = request.FILES['foto']
                    print(imagefile)
                    fs = FileSystemStorage()
                    filename = fs.save(imagefile.name, imagefile)
                    if (filename is not None) and (filename != ""):
                        lider.foto = filename
            
            lider.save()
            print(f"Lider {nome} salvo com sucesso!")

        except Exception as e:
            print(f"Erro ao salvar lider: {e}")
        return redirect("lider-create")

    return render(request, template_name="lider/lider-create.html", status=200)

@planejador_required
def lider_edit(request, email):
    # Verifica se o email foi passado corretamente
    print(f"email recebido: {email}")
    lider = get_object_or_404(Lider, email=email)

    if request.method == "POST":
        # Recebendo dados do formulário
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        profissao = request.POST.get("profissao")
        senha = request.POST.get("senha")
        foto = request.FILES.get("foto")

        try:
            # Atualizando campos
            lider.nome = nome if nome else lider.nome  # Mantém o nome anterior se não for enviado

            lider.email = email if email else lider.email  # Mantém o email anterior se não for enviado
            lider.profissao = profissao if profissao else lider.profissao  # Mantém a profissão anterior se não for enviada
            lider.senha = senha if senha else lider.senha  # Mantém a senha anterior se não for enviada

            # Verifica se uma nova foto foi fornecida
            if foto:
                lider.foto = foto
            # Se não, mantém a foto anterior

            lider.save()
            print(f"lider {nome} atualizado com sucesso!")
            return redirect('lider-manage')

        except Exception as e:
            print(f"Erro ao atualizar lider: {e}")
            return HttpResponse("Erro ao salvar lider", status=400)

    return render(request, 'lider/lider-edit.html', {'lider': lider})

@planejador_required
def lider_delete(request, email):
    lider = get_object_or_404(Lider, email=email)
    foto_path = lider.foto.path
        
    if os.path.exists(foto_path):
        print(lider.foto.path)
        os.remove(foto_path)  
    
    lider.delete()
    return redirect("lider-manage")