from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .Colaborador import Colaborador
from .Lider import Lider
from .Planejador import Planejador
from .Tarefa import Tarefa
from .TarefaColaborador import TarefaColaborador