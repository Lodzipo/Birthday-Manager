from django.contrib.auth.models import AbstractUser, BaseUserManager


class MyUserManager(BaseUserManager):
    """
    Кастомный менеджер для управления пользователями.
    Позволяет создавать обычных пользователей и суперпользователей.
    """

    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        """Создаёт и возвращает обычного пользователя."""
        if not username:
            raise ValueError("The Username field is required")
        email = self.normalize_email(email)  # Приведение email к стандартному формату.
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Установка пароля пользователя.
        user.save(using=self._db)  # Сохранение пользователя в базу данных.
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Создаёт и возвращает суперпользователя."""
        extra_fields.setdefault("is_staff", True)  # Устанавливает is_staff=True.
        extra_fields.setdefault(
            "is_superuser", True
        )  # Устанавливает is_superuser=True.

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class MyUser(AbstractUser):
    """Кастомная модель пользователя, использующая MyUserManager для управления."""

    objects = MyUserManager()  # Заменяем стандартный менеджер на кастомный.
