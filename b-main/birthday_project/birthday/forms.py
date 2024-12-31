from django import forms

from .models import Birthday, Congratulation


class BirthdayForm(forms.ModelForm):
    """
    Форма для создания и редактирования записей о днях рождения.
    Использует модель `Birthday` для автоматической генерации полей формы.
    """

    class Meta:
        """
        Вложенный класс для указания модели и настройки отображения полей формы.
        """
        # Указываем модель, на основе которой строится форма
        model = Birthday
        # Исключаем поле "author", так как оно заполняется автоматически
        exclude = ("author",)
        # Указываем, что все остальные поля модели отображаются
        fields = "__all__"
        # Настраиваем виджет для поля "birthday"
        widgets = {
            "birthday": forms.DateInput(
                attrs={
                    "type": "date",  # Указываем тип input для календаря
                    "class": "form-control",  # Стилизация через Bootstrap
                }
            )
        }

    def clean_first_name(self):
        """
        Проверяет значение поля "first_name".
        Возвращает только первое слово из введённого текста, если пользователь ввёл больше одного слова.
        """
        # Получаем значение поля "first_name"
        first_name = self.cleaned_data["first_name"]
        # Возвращаем первое слово из строки
        return first_name.split()[0]

    
class CongratulationForm(forms.ModelForm):
    """
    Форма для создания поздравлений.

    Использует модель `Congratulation` и позволяет вводить только текст поздравления.
    """

    class Meta:
        """
        Вложенный класс для указания модели и отображаемых полей.
        """
        # Указываем модель Congratulation
        model = Congratulation
        # Отображается только поле "text"
        fields = ("text",)
