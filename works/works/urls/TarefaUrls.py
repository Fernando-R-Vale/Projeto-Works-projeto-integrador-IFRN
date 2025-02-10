from django.urls import path
from works.views.TarefaView import *
urlpatterns = [
    path('tarefa-details/', list_tarefas_view, name='tarefa-details'),
    path('tarefa-edit/<int:id>/', tarefa_edit, name='tarefa-edit'),
    path('tarefa-delete/<int:id>/', tarefa_delete, name='tarefa-edit'),
    path('tarefa-create/', create_tarefas_view, name='tarefa-create'),
    path('registro-tarefa/<int:id>/', registro_tarefa_view, name='registro-tarefas'),
    path("editar-tarefa/<int:id>/", editar_registrar_view, name="editar-tarefa"),
    path('home-lider/', home_lider_view, name='home-lider'),
    path('visualizar tarefa/<int:id>/', visualizar_tarefa_view, name='visualizar-tarefa'),
]

