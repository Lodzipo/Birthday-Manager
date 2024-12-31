from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("pages:homepage")

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()
        # Выполняем вход
        login(self.request, user)
        return super().form_valid(form)
