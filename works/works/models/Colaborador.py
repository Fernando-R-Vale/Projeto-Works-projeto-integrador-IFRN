from works.models import *

class Colaborador(models.Model):
    nome = models.CharField(null=False, max_length=100)
    dt_nascimento = models.DateField(null=False)
    cpf = models.CharField(null=False, max_length=14, primary_key=True)
    profissao = models.CharField(null=False, max_length=70)
    descricao = models.CharField(null=True, max_length=300, blank=True)
    foto = models.ImageField(null=False, blank=True)

    def __str__(self):
        return '{}'.format(self.nome)