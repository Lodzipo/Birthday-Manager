from django.urls import path

from . import views

app_name = 'pages'

# Маршрут главной страницы
urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
]
