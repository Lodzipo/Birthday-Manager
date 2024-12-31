from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import CustomUserCreationForm

# Устанавливаем обработчик для ошибки 404 (страница не найдена)
handler404 = "core.views.page_not_found"

# Определяем основные маршруты (URL-ы) проекта
urlpatterns = [
    path("", include("pages.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "auth/registration/",  # URL-адрес для регистрации
        CreateView.as_view(
            template_name="registration/registration_form.html",
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy("pages:homepage"),
        ),
        name="registration",
    ),
    path("birthday/", include("birthday.urls")),
] 

# Добавляем поддержку медиа-файлов (например, для загрузки изображений) в режиме разработки
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
