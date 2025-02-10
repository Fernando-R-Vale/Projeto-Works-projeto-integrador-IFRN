from django.shortcuts import render
from works.decorators import planejador_required
@planejador_required
def home_view(request):
    return render(request, template_name='home/home.html', status=200)