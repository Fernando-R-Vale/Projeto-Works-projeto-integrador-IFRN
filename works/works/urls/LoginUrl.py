from django.urls import path
from works.views.LoginView import *
urlpatterns = [
    path('', login, name='login'),
    path('logout/', logout, name='logout'), 
]
