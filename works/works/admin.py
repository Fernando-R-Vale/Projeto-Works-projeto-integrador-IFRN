from django.contrib import admin
from .models import *
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dt_nascimento', 'cpf', 'profissao', 'descricao', 'foto')
    empty_value_display = 'Vazio'
    search_fields = ('nome', 'cpf', 'profissao')

class LiderAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'senha', 'foto')
    empty_value_display = 'Vazio'
    search_fields = ('nome', )
class PlanejadorAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'senha')
    empty_value_display = 'Vazio'
    search_fields = ('nome', 'email')
class TarefaAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'status','descricao', 'ocorrencia', 'dh_inicio', 'dh_termino', 'planejador_email', 'lider_email')
    date_hierarchy = 'dh_cadastro'
    empty_value_display = 'Vazio'
    search_fields = ('nome', 'status', 'lider_email', 'planejador_email')
class TarefaColaboradorAdmin(admin.ModelAdmin):
    list_display = ('tarefa', 'colaborador')
    search_fields = ('tarefa', 'colaborador')

admin.site.register(Colaborador, ColaboradorAdmin)
admin.site.register(Lider, LiderAdmin)
admin.site.register(Planejador, PlanejadorAdmin)
admin.site.register(Tarefa, TarefaAdmin)
admin.site.register(TarefaColaborador, TarefaColaboradorAdmin)