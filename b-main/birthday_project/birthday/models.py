from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .validators import real_age

# Получаем пользовательскую модель User
User = get_user_model()


class Tag(models.Model):
    """
    Модель для хранения тегов, связанных с днями рождения.
    """

    tag = models.CharField("Тег", max_length=20)

    def __str__(self):
        """
        Возвращает строковое представление объекта.
        """
        return self.tag


class Birthday(models.Model):
    """
    Модель для хранения информации о дне рождения.

    Поля:
    - author: Пользователь, создавший запись.
    - first_name: Имя человека.
    - last_name: Фамилия человека (необязательное поле).
    - birthday: Дата рождения с проверкой реальности возраста через валидатор.
    - image: Фото, связанное с записью.
    - tags: Теги, описывающие связь "многие ко многим".
    """

    author = models.ForeignKey(
        User, verbose_name="Автор записи", on_delete=models.CASCADE
    )
    first_name = models.CharField("Имя", max_length=20)
    last_name = models.CharField(
        "Фамилия", max_length=20, help_text="Необязательное поле", blank=True
    )
    birthday = models.DateField("Дата рождения", validators=(real_age,))
    image = models.ImageField("Фото", upload_to="birthdays_images", blank=True)
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
        blank=True,
        help_text="Удерживайте Ctrl для выбора нескольких вариантов",
    )

    class Meta:
        """
        Метаданные модели Birthday:
        - ordering: Сортировка записей по дате рождения.
        - constraints: Уникальность имени, фамилии и даты рождения.
        """

        ordering = ["birthday"]
        constraints = (
            models.UniqueConstraint(
                fields=("first_name", "last_name", "birthday"),
                name="Unique person constraint",
            ),
        )

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для детального представления записи о дне рождения.
        """
        return reverse("birthday:detail", kwargs={"pk": self.pk})


class Congratulation(models.Model):
    """
    Модель для хранения поздравлений, связанных с днём рождения.

    Поля:
    - text: Текст поздравления.
    - birthday: Связь с записью о дне рождения через связь "многие к одному".
    - created_at: Дата и время создания поздравления.
    - author: Пользователь, создавший поздравление.
    """

    text = models.TextField("Текст поздравления")
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name="congratulations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """
        Метаданные модели Congratulation:
        - ordering: Сортировка поздравлений по дате создания.
        """

        ordering = ("created_at",)
