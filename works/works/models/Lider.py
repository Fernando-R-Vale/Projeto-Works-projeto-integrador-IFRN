from works.models import *

class Lider(models.Model):
    foto = models.ImageField(null=False)
    nome = models.CharField(null=False, max_length=100)
    email = models.EmailField(null=False, max_length=100, primary_key=True)
    senha = models.CharField(null=False, max_length=12)
    profissao = models.CharField(null=False, max_length=70)

    def __str__(self):
        return '{}'.format(self.email)