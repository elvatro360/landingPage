from django.urls import path
from . import views


urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('about/', views.about, name='about' ),
    path('legal/', views.legal, name='legal'),
    path('contacto/', views.contact_view, name='contacto'),
]