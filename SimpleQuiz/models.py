from django.db.models.aggregates import Count
from random import randint
from django.db import models
from Account.models import Account
from ThemedQuiz.models import ANSWER

LANGUAGE = (
    ('E', 'English'),
    ('R', 'Russian'),
)


class QuestionHeaderManager(models.Manager):
    def random_100(self):
        # count = self.aggregate(count=Count('id'))['count']
        count = self.aggregate(count=Count('id'))[100]
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class QuestionHeader(models.Model):
    active = models.BooleanField(default=False, verbose_name='Опубликовано', help_text='Установите флаг для публикации вопроса')
    description = models.CharField(verbose_name='Описание', max_length=500, help_text='Короткое описание вопроса')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Account, blank=True, null=True, related_name='question_header_owner', verbose_name='Создатель', help_text='Создатель')

    objects = QuestionHeaderManager()

    class Meta:
        verbose_name = 'Группы вопросов'
        verbose_name_plural = 'Группы вопросов'


class Questions(models.Model):
    header = models.ForeignKey(QuestionHeader, null=True, related_name='question_header')
    language = models.CharField(verbose_name='Язык', max_length=1, choices=LANGUAGE, help_text='Язык вопроса')
    question = models.TextField(verbose_name='Вопрос', help_text='Текс вопроса', max_length=500)
    answer1 = models.TextField(verbose_name='Ответ №1', max_length=500, help_text='Текс варианта ответа №1')
    answer2 = models.TextField(verbose_name='Ответ №2', max_length=500, help_text='Текс варианта ответа №2')
    right_answer = models.IntegerField(choices=ANSWER, verbose_name='Правильный ответ', help_text='Номер правильного ответа')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Account, blank=True, null=True, related_name='question_body_owner', verbose_name='Создатель', help_text='Создатель')

    class Meta:
        unique_together = (("header", "language"),)
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
