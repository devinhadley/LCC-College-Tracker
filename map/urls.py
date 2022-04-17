from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/submit', views.process_entry, name='processEntry'),
]