from django.contrib import admin
from django.db import models
from django.forms.widgets import Textarea

from SimpleQuiz.models import Questions, QuestionHeader


# # Register your models here.
# class CityAdmin(admin.ModelAdmin):
#     list_display = ('country', 'name', 'created_at', 'updated_at')
#     list_display_links = ('country', 'name', 'created_at', 'updated_at')
#     list_filter = ('country',)

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('language', 'question', 'answer1', 'answer2', 'right_answer', 'owner', 'created_at',)
    list_filter = ('language', 'owner',)
    search_fields = ['question', 'answer1', 'answer2', ]
    model = Questions

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()


class QuestionsAdminInline(admin.TabularInline):
    list_display = ('language', 'question', 'answer1', 'answer2', 'right_answer')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 30})},
    }
    model = Questions

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()


class HeaderQuestionAdmin(admin.ModelAdmin):
    list_display = ('description', 'active', 'owner', 'created_at', 'updated_at')
    list_filter = ('description', 'active', 'owner',)
    search_fields = ['description', 'created_at']
    inlines = [
        QuestionsAdminInline,
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

admin.site.register(QuestionHeader, HeaderQuestionAdmin)
admin.site.register(Questions, QuestionsAdmin)
