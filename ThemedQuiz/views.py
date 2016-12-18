import datetime

from rest_framework import filters
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from ThemedQuiz.models import DayTheme, DayThemeTranslation, DayQuestions
from ThemedQuiz.serializers import DayThemeSerializer, DayQuestionsSerializer, DayThemeTranslationSerializer


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

        day_val = self.request.query_params.get('day', None)
        month_val = self.request.query_params.get('month', None)
        year_val = self.request.query_params.get('year', None)

        try:
            if day_val is not None and month_val is not None and year_val is not None:
                target_theme = DayTheme.objects.filter(target_date__day=day_val, target_date__month=month_val, target_date__year=year_val, active=True)
            else:
                target_theme = DayTheme.objects.filter(target_date__day=today.day, target_date__month=today.month, target_date__year=today.year, active=True)
        except ValueError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if target_theme.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if p_language is None or p_language not in ['E', 'R']:
            p_language = 'E'

        theme_translation = DayThemeTranslation.objects.filter(language=p_language, theme=target_theme[0])
        if theme_translation.count() > 0:

            questions_by_language = DayQuestions.objects.filter(header__active=True, language=p_language, header__theme=target_theme[0])
            if questions_by_language.count() > 0:

                serializer_theme = DayThemeTranslationSerializer(theme_translation[0])
                serializer_question = DayQuestionsSerializer(questions_by_language, many=True)
                return Response({"theme": serializer_theme.data, "questions": serializer_question.data})
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['get'], url_path='get-changed-theme-questions/(?P<p_language>[A-Z]+)')
    def get_changed_themes_questions(self, request, p_language=None):

        if p_language is None or p_language not in ['E', 'R']:
            p_language = 'E'

        today = datetime.datetime.today()

        day_val = self.request.query_params.get('day', None)
        month_val = self.request.query_params.get('month', None)
        year_val = self.request.query_params.get('year', None)

        create_day_val = self.request.query_params.get('create_day', None)
        create_month_val = self.request.query_params.get('create_month', None)
        create_year_val = self.request.query_params.get('create_year', None)

        try:
            if day_val is not None and month_val is not None and year_val is not None:
                max_change_date = datetime.date(year=int(year_val), month=int(month_val), day=int(day_val))
            else:
                max_change_date = datetime.date(year=today.year, month=today.month, day=today.day)

            if create_day_val is not None and create_month_val is not None and create_year_val is not None:
                max_create_date = datetime.date(year=int(create_year_val), month=int(create_month_val), day=int(create_day_val))
            else:
                max_create_date = datetime.date(year=today.year, month=today.month, day=today.day)

        except ValueError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        changed_questions = DayQuestions.objects.filter(created_at__lte=max_create_date, updated_at__gt=max_change_date, header__active=True, header__theme__active=True, language=p_language)
        themes_by_interval = DayTheme.objects.filter(created_at__lte=max_create_date, updated_at__gt=max_change_date, active=True)

        # header_ids = list(changed_questions.values_list("header_id", flat=True))
        theme_list = []
        for quest in changed_questions:
            theme_list.append(quest.header.theme)

        for theme_c in themes_by_interval:
            theme_list.append(theme_c)

        output = set()
        for x in theme_list:
            output.add(x)

        theme_list = list(output)

        changed_themes = []
        for theme in theme_list:
            theme_translation = DayThemeTranslation.objects.filter(language=p_language, theme=theme)

            if theme_translation.count() > 0:
                questions_by_language = DayQuestions.objects.filter(header__active=True, language=p_language, header__theme=theme)

                if questions_by_language.count() > 0:
                    serializer_theme = DayThemeTranslationSerializer(theme_translation[0])
                    serializer_question = DayQuestionsSerializer(questions_by_language, many=True)
                    changed_themes.append({"theme": serializer_theme.data, "questions": serializer_question.data})

        if len(changed_themes) > 0:
            return Response(changed_themes)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['get'], url_path='get-theme-questions-interval/(?P<p_language>[A-Z]+)')
    def get_themes_questions_by_interval(self, request, p_language=None):

        if p_language is None or p_language not in ['E', 'R']:
            p_language = 'E'

        today = datetime.datetime.today()

        last_day_val = self.request.query_params.get('last_day', None)
        last_month_val = self.request.query_params.get('last_month', None)
        last_year_val = self.request.query_params.get('last_year', None)

        current_day_val = self.request.query_params.get('current_day', None)
        current_month_val = self.request.query_params.get('current_month', None)
        current_year_val = self.request.query_params.get('current_year', None)

        try:
            if last_year_val is not None or last_month_val is not None or last_day_val is not None:
                last_date = datetime.date(year=int(last_year_val), month=int(last_month_val), day=int(last_day_val))
            else:
                last_date = None

            if current_year_val is not None:
                current_date = datetime.date(year=int(current_year_val), month=int(current_month_val), day=int(current_day_val))
            else:
                current_date = datetime.date(year=today.year, month=today.month, day=today.day)

        except ValueError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if last_date is not None:
            # themes_by_interval = DayTheme.objects.filter(target_date__range=[last_date, current_date], active=True)
            themes_by_interval = DayTheme.objects.filter(target_date__gt=last_date, target_date__lt = current_date, active=True)
        else:
            themes_by_interval = DayTheme.objects.filter(target_date__lt=current_date, active=True)

        theme_list = themes_by_interval

        changed_themes = []
        for theme in theme_list:
            theme_translation = DayThemeTranslation.objects.filter(language=p_language, theme=theme)

            if theme_translation.count() > 0:
                questions_by_language = DayQuestions.objects.filter(header__active=True, language=p_language, header__theme=theme)

                if questions_by_language.count() > 0:
                    serializer_theme = DayThemeTranslationSerializer(theme_translation[0])
                    serializer_question = DayQuestionsSerializer(questions_by_language, many=True)
                    changed_themes.append({"theme": serializer_theme.data, "questions": serializer_question.data})

        if len(changed_themes) > 0:
            return Response(changed_themes)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
