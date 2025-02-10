from works.models import *

class Planejador(models.Model):
    email = models.CharField(null=False, max_length=100, primary_key=True)
    nome = models.CharField(null=False, max_length=100)
    senha = models.CharField(null=False, max_length=12)

    def __str__(self):
        return '{}'.format(self.email)