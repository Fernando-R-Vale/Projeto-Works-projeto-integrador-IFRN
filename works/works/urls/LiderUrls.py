from django.urls import path
from works.views.LiderView import *
urlpatterns = [
    path('lider-manage', list_lideres, name='lider-manage'),
    path('lider-create', create_lider_view, name='lider-create'),
    path('lider-edit/<str:email>/', lider_edit, name='lider-edit'),
    path('lider-delete/<str:email>/', lider_delete, name='lider-delete')
]