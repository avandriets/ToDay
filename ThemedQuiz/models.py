from django.db import models

from Account.models import Account

LANGUAGE = (
    ('E', 'English'),
    ('R', 'Russian'),
)

ANSWER = (
    (1, '1'),
    (2, '2'),
)


class DayTheme(models.Model):
    target_date = models.DateField(verbose_name='Дата темы', help_text='Дата с которой будет активна тема')
    imageURL = models.FileField(verbose_name='Изображение', null=True, blank=True)
    active = models.BooleanField(default=False, verbose_name='Опубликовано', help_text='Установите флаг для публикации темы')
    description = models.CharField(verbose_name='Описание', max_length=500, help_text='Короткое описание темы')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Account, null=True, blank=True, related_name='day_them_owner', verbose_name='Создатель', help_text='Создатель')

    class Meta:
        verbose_name = 'Тема дня'
        verbose_name_plural = 'Тема дня'

    def __str__(self):
        return self.description + " - " + self.target_date.strftime("%B %d, %Y")


class DayThemeTranslation(models.Model):
    theme = models.ForeignKey(DayTheme, null=True, related_name='question_theme')
    language = models.CharField(verbose_name='Язык', max_length=1, choices=LANGUAGE, help_text='Язык')
    name = models.CharField(verbose_name='Название темы', max_length=500, help_text='Название темы')
    description = models.TextField(null=True, blank=True, verbose_name='Описание', max_length=500, help_text='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Account, null=True, blank=True, related_name='day_them_translation_owner')

    class Meta:
        unique_together = (("theme", "language"),)
        verbose_name = 'Перевод темы дня'
        verbose_name_plural = 'Переводы темы дня на другой язык'


class DayQuestionHeader(models.Model):
    theme = models.ForeignKey(DayTheme, null=True, related_name='question_day_theme')
    active = models.BooleanField(default=False, verbose_name='Опубликовано', help_text='Установите флаг для публикации вопроса')
    description = models.CharField(verbose_name='Описание', max_length=500, help_text='Описание вопроса')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Account, null=True, blank=True, related_name='day_question_header_owner')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class DayQuestions(models.Model):
    header = models.ForeignKey(DayQuestionHeader, null=True, related_name='day_question_header')
    language = models.CharField(verbose_name='Язык', max_length=1, choices=LANGUAGE, help_text='Язык')
    question = models.TextField(verbose_name='Вопрос', max_length=500, help_text='Вопрос')
    answer1 = models.TextField(verbose_name='Ответ 1', max_length=500, help_text='Ответ 1')
    answer2 = models.TextField(verbose_name='Ответ 2', max_length=500, help_text='Ответ 2')
    right_answer = models.IntegerField(choices=ANSWER)
    description = models.TextField(null=True, blank=True, verbose_name='Описание', max_length=500, help_text='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Account, null=True, blank=True, related_name='day_question_body_owner')

    class Meta:
        unique_together = (("header", "language"),)
        verbose_name = 'Содержание вопроса'
        verbose_name_plural = 'Содержание вопросов'
