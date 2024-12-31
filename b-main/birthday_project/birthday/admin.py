from django.contrib import admin

from .models import Birthday, Tag

admin.site.empty_value_display = "Не задано"

# Админ панель проекта

@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birthday")
    search_fields = ("first_name", "last_name")
    ordering = ("first_name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    ordering = ('tag',)
