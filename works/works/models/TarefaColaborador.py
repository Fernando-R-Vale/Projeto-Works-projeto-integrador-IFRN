from works.models import *

class TarefaColaborador(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)

    def __str__(self):
        return f'Tarefa {self.tarefa.id} - Colaborador {self.colaborador.nome}'