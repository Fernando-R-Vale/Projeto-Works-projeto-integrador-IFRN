from django.urls import path
from works.views.SenhaView import *
urlpatterns = [
    path('digitar-email/', digitar_email, name='digitar-email'),
    path('verificar-codigo/', verificar_codigo, name='verificar-codigo'),
    path('nova-senha/', nova_senha, name='nova_senha'),
    path('recuperacao-sucesso/', recuperacao_sucesso, name='recuperacao_sucesso'),
]
