import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import list_route
from rest_framework.response import Response

from ThemedQuiz.models import DayTheme, DayThemeTranslation, DayQuestions
from ThemedQuiz.serializers import DayThemeSerializer, DayQuestionsSerializer, DayThemeTranslationSerializer
from rest_framework import permissions


class DayThemeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DayTheme.objects.all()
    serializer_class = DayThemeSerializer

    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ('created_at', 'updated_at')

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = DayTheme.objects.all()
        return queryset

    @list_route(methods=['get'], url_path='get-day-theme-questions/(?P<p_language>[A-Z]+)')
    def get_day_theme_questions(self, request, p_language=None):

        today = datetime.datetime.today()

        day_val = self.request.query_params.get('day', today.day)
        month_val = self.request.query_params.get('month', today.month)
        year_val = self.request.query_params.get('year', today.year)

        target_theme = DayTheme.objects.filter(target_date__day=day_val, target_date__month=month_val, target_date__year=year_val, active=True)

        if target_theme.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if p_language is None or p_language not in ['E','R']:
            p_language = 'E'

        theme_translation = DayThemeTranslation.objects.filter(language=p_language, theme=target_theme[0])
        if theme_translation.count() > 0:

            questions_by_language = DayQuestions.objects.filter(header__active=True, language=p_language, header__theme=target_theme[0])
            if questions_by_language.count() > 0:

                serializer_theme = DayThemeTranslationSerializer(theme_translation, many=True)
                serializer_question = DayQuestionsSerializer(questions_by_language, many=True)
                return Response({ "theme": serializer_theme.data, "questions": serializer_question.data})
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['get'], url_path='get-changed-theme-questions/(?P<p_language>[A-Z]+)')
    def get_changed_themes_questions(self, request, p_language=None):

        if p_language is None or p_language not in ['E','R']:
            p_language = 'E'

        today = datetime.datetime.today()

        day_val = self.request.query_params.get('day', today.day)
        month_val = self.request.query_params.get('month', today.month)
        year_val = self.request.query_params.get('year', today.year)

        max_change_date = datetime.date(year=year_val, month=month_val, day=day_val)

        changed_questions = DayQuestions.objects.filter(updated_at__gt=max_change_date, header__active=True, header__theme__active=True, language=p_language)

        # header_ids = list(changed_questions.values_list("header_id", flat=True))
        theme_list = []
        for quest in changed_questions:
            theme_list.append(quest.header.theme)

        changed_themes = []
        for theme in theme_list:
            theme_translation = DayThemeTranslation.objects.filter(language=p_language, theme=theme)
            questions_by_language = DayQuestions.objects.filter(header__active=True, language=p_language, header__theme=theme)

            serializer_theme = DayThemeTranslationSerializer(theme_translation, many=True)
            serializer_question = DayQuestionsSerializer(questions_by_language, many=True)

            changed_themes.append({"theme": serializer_theme.data, "questions": serializer_question.data})

        if len(changed_themes) > 0:
            return Response(changed_themes)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)