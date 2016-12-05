from django.contrib import admin
from django.db import models
from django.forms.widgets import Textarea

from ThemedQuiz.models import DayTheme, DayThemeTranslation, DayQuestionHeader, DayQuestions


class DayThemeTranslationAdminInline(admin.TabularInline):
    list_display = ('language', 'name', 'description' 'created_at', 'updated_at', 'owner', )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 30})},
    }
    model = DayThemeTranslation


class DayThemeAdmin(admin.ModelAdmin):
    list_display = ('target_date', 'main_theme', 'active', 'imageURL',
                    'backgroundImageURL',
                    'description', 'owner', 'created_at', 'updated_at')
    list_filter = ('active', 'owner',)
    search_fields = ['description', ]
    inlines = [
        DayThemeTranslationAdminInline,
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if instance.owner is None:
                instance.owner = request.user
            instance.save()
        formset.save_m2m()


class ThemeQuestionAdmin(admin.TabularInline):
    list_display = ('language', 'question', 'answer1', 'answer2', 'right_answer', 'description')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 30})},
    }
    model = DayQuestions


class ThemeQuestionHeaderAdmin(admin.ModelAdmin):
    list_display = ('theme', 'active', 'description', 'created_at', 'updated_at', 'owner', )
    list_filter = ('active', 'owner', 'theme',)
    search_fields = ['description', ]

    inlines = [
        ThemeQuestionAdmin,
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if instance.owner is None:
                instance.owner = request.user
            instance.save()
        formset.save_m2m()


admin.site.register(DayTheme, DayThemeAdmin)
admin.site.register(DayQuestionHeader, ThemeQuestionHeaderAdmin)