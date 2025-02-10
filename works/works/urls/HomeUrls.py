from django.urls import path
from works.views.HomeView import home_view
urlpatterns = [
    path("", home_view, name='home'),
]