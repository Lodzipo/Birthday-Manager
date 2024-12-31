from datetime import date

from django.core.exceptions import ValidationError


def real_age(value: date) -> None:
    """Валидатор для проверки возраста на основе даты рождения."""
    # Вычисляем возраст в годах
    age = (date.today() - value).days / 365
    # Проверяем, находится ли возраст в допустимых пределах
    if age < 0 or age > 120:
        raise ValidationError(
            'Ожидается возраст от 1 года до 120 лет'
        )
