from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = "birthday"

# Определяем маршруты проекта
urlpatterns = [
    path('create/', views.BirthdayCreateView.as_view(), name='create'),
    path("list/", views.BirthdayListView.as_view(), name="list"),
    path("<int:pk>/", views.BirthdayDetailView.as_view(), name="detail"),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path("<int:pk>/edit/", views.BirthdayUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.BirthdayDeleteView.as_view(), name="delete"),
]