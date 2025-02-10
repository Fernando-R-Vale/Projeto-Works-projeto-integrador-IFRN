from django.urls import path
from works.views.ColaboradorView import *
urlpatterns = [
    path('colaborador-manage', list_colaboradores, name='colaborador-manage'),
    path('colaborador-create', create_colaborador_view, name='colaborador-create'),
    path('colaborador-edit/<str:cpf>/', colaborador_edit, name='colaborador-edit'),
    path('colaborador-delete/<str:cpf>/', colaborador_delete, name='colaborador-delete'),
    # path('colaborador-details/<int:id>/', colaborador_details, name='colaborador-details'),
]