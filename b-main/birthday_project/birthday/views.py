from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday
from .utils import calculate_birthday_countdown


class OnlyAuthorMixin(UserPassesTestMixin):
    """
    Миксин для проверки, что текущий пользователь является автором объекта.
    Используется для ограничения доступа к изменениям объектов.
    """

    def test_func(self):
        """Проверяет, совпадает ли автор объекта с текущим пользователем."""
        object = self.get_object()
        return object.author == self.request.user


@login_required
def add_comment(request, pk):
    """
    Обрабатывает добавление комментария (поздравления) к записи о дне рождения.

    Доступно только для авторизованных пользователей и обрабатывает POST-запросы.
    """
    birthday = get_object_or_404(Birthday, pk=pk)
    form = CongratulationForm(request.POST)
    if form.is_valid():
        congratulation = form.save(commit=False)
        congratulation.author = request.user
        congratulation.birthday = birthday
        congratulation.save()
    return redirect("birthday:detail", pk=pk)


class BirthdayListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка записей о днях рождения.

    Ограничивает доступ только для авторизованных пользователей.
    Сортирует записи по дате рождения и разбивает их на страницы.
    """

    model = Birthday
    ordering = "birthday"
    paginate_by = 10

    def get_queryset(self):
        """Возвращает записи, принадлежащие текущему пользователю."""
        return (
            Birthday.objects.filter(author=self.request.user)
            .prefetch_related("tags")
            .select_related("author")
        )

    def get_context_data(self, **kwargs):
        """Добавляет общее количество записей текущего пользователя в контекст."""
        context = super().get_context_data(**kwargs)
        context["total_count"] = Birthday.objects.filter(
            author=self.request.user
        ).count()
        return context


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой записи о дне рождения.

    Автоматически добавляет текущего пользователя как автора записи.
    """

    model = Birthday
    form_class = BirthdayForm
    success_url = reverse_lazy("birthday:list")

    def form_valid(self, form):
        """Добавляет текущего пользователя как автора записи перед сохранением."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    """
    Представление для редактирования записи о дне рождения.

    Доступно только автору записи.
    """

    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(OnlyAuthorMixin, LoginRequiredMixin, DeleteView):
    """
    Представление для удаления записи о дне рождения.

    Доступно только автору записи.
    """

    model = Birthday
    success_url = reverse_lazy("birthday:list")


class BirthdayDetailView(DetailView):
    """
    Представление для отображения детальной информации о записи о дне рождения.

    Добавляет в контекст обратный отсчёт до следующего дня рождения,
    форму для добавления поздравления и список всех поздравлений.
    """

    model = Birthday

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст: обратный отсчёт до дня рождения,
        форма поздравления и список поздравлений.
        """
        context = super().get_context_data(**kwargs)
        context["birthday_countdown"] = calculate_birthday_countdown(
            self.object.birthday
        )
        context["form"] = CongratulationForm()
        context["congratulations"] = self.object.congratulations.select_related(
            "author"
        )
        return context
