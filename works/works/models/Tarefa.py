from works.models import *

class Tarefa(models.Model):
    status = models.CharField(null=False, max_length=12)
    dh_cadastro = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(null=False, max_length=100)
    descricao = models.CharField(null=True, max_length=300, blank=True)
    ocorrencia = models.CharField(null=True, max_length=300, blank=True)
    dh_inicio = models.DateTimeField()
    dh_termino = models.DateTimeField()
    planejador_email = models.ForeignKey(Planejador, null=True, related_name='planejador_email', on_delete=models.SET_NULL)
    lider_email = models.ForeignKey(Lider, null=True, related_name='lider_email', on_delete=models.SET_NULL)
    colaboradores = models.ManyToManyField('Colaborador', through='TarefaColaborador', related_name='tarefas')
    cadastro_realizado = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.id)
