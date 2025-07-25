from django.urls import path
from . import views

app_name = 'braille_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('suggestions/', views.get_suggestions, name='get_suggestions'),
    path('convert/', views.convert_text, name='convert_text'),
]
